import argparse
from concurrent.futures import ProcessPoolExecutor
import functools
import logging
import multiprocessing
import os

from intervaltree import IntervalTree, Interval
import numpy as np
import pysam


from pomoxis.util import parse_regions, Region, filter_args, filter_read, write_bam
from pomoxis.coverage_from_bam import coverage_summary_of_region


def main():
    logging.basicConfig(format='[%(asctime)s - %(name)s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    parser = argparse.ArgumentParser(
        prog='subsample_bam',
        description='Subsample a bam to uniform or proportional depth',
        parents=[filter_args()],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('bam',
        help='input bam file.')
    parser.add_argument('depth', nargs='+', type=int,
        help='Target depth.')
    parser.add_argument('-o', '--output_prefix', default='sub_sampled',
        help='Output prefix')
    parser.add_argument('-r', '--regions', nargs='+',
        help='Only process given regions.')
    parser.add_argument('-p', '--profile', type=int, default=1000,
        help='Stride in genomic coordinates for depth profile.')
    parser.add_argument('-t', '--threads', type=int, default=-1,
        help='Number of threads to use.')
    parser.add_argument('--force_low_depth', action='store_true',
        help='Force saving reads mapped to a sequence with coverage below the expected value.')

    eparser = parser.add_mutually_exclusive_group()
    eparser.add_argument('--any_fail', action='store_true',
        help='Exit with an error if any region has insufficient coverage.')
    eparser.add_argument('--all_fail', action='store_true',
        help='Exit with an error if all regions have insufficient coverage.')

    uparser = parser.add_argument_group('Uniform sampling options')
    uparser.add_argument('-x', '--patience', default=5, type=int,
        help='Maximum iterations with no change in median coverage before aborting.')
    uparser.add_argument('-s', '--stride', type=int, default=1000,
        help='Stride in genomic coordinates when searching for new reads. Smaller can lead to more compact pileup.')

    pparser = parser.add_argument_group('Proportional sampling options')
    pparser.add_argument('-P', '--proportional', default=False, action='store_true',
        help='Activate proportional sampling, thus keeping depth variations of the pileup.')
    pparser.add_argument('-S', '--seed', default=None, type=int,
        help='Random seed for proportional downsampling of reads.')

    args = parser.parse_args()
    if args.threads == -1:
        args.threads = multiprocessing.cpu_count()

    with pysam.AlignmentFile(args.bam) as bam:
        ref_lengths = dict(zip(bam.references, bam.lengths))

        if args.regions is not None:
            regions = parse_regions(args.regions, ref_lengths=ref_lengths)
        else:
            regions = [Region(ref_name=r, start=0, end=ref_lengths[r]) for r in bam.references]

    if args.proportional:
        worker = functools.partial(subsample_region_proportionally, args=args)
    else:
        worker = functools.partial(subsample_region_uniformly, args=args)

    enough_depth = []
    with ProcessPoolExecutor(max_workers=args.threads) as executor:
        for res in executor.map(worker, regions):
            enough_depth.append(res)

    if args.any_fail and not all(enough_depth):
        raise RuntimeError('Insufficient read coverage for one or more requested regions.')
    if args.all_fail and all([not x for x in enough_depth]):
        raise RuntimeError('Insufficient read coverage for all requested regions.')


def subsample_region_proportionally(region, args):
    logger = logging.getLogger(region.ref_name)
    coverage_summary = coverage_summary_of_region(
        region, args.bam, args.stride, functools.partial(filter_read, args=args, logger=logger))
    col = 'depth_{}'.format(args.orientation) if args.orientation is not None else 'depth'
    median_coverage = coverage_summary[col].T['50%']
    logger.info(f'Median coverage {median_coverage}')
    with pysam.AlignmentFile(args.bam) as bam:
        def _read_iter():
            for r in bam.fetch(region.ref_name, region.start, region.end):
                if not filter_read(r, args, logger):
                    yield r
        # Prepare iterator
        reads = _read_iter()
        # query names cannot be longer than 251
        dtype = [('name', 'U251'), ('start', int), ('end',  int)]
        read_data = np.fromiter(
            ((r.query_name, r.reference_start, r.reference_end) for r in reads),
            dtype=dtype
        )
        if len(read_data) == 0:
            logger.warn(f'No primary reads found in {region.ref_name}.')
            found_enough_depth = False
            return found_enough_depth

    targets = sorted(args.depth)
    found_enough_depth = True

    coverage = np.zeros(region.end - region.start, dtype=np.uint16)
    if args.seed is not None:
        np.random.seed(args.seed)

    for target in targets:
        if target > median_coverage:
            found_enough_depth = False
            if not args.force_low_depth:
                msg = 'Target depth {} exceeds median coverage, limiting to {} and skipping higher depths.'
                logger.warn(msg.format(target, int(median_coverage)))
                break
        fraction = target / median_coverage
        if fraction <= 1:
            n_reads = int(round(fraction * len(read_data), 0))
            target_reads = np.random.choice(read_data, n_reads, replace=False)
            logger.info('Processing {}X: {} reads ({:.2f} %).'.format(target, n_reads, 100 * fraction))
        else:
            n_reads = len(read_data)
            target_reads = read_data
            found_enough_depth = False
            logger.warn('Insufficient coverage: {} reads ({}X).'.format(n_reads, median_coverage))
        if found_enough_depth:
            prefix = '{}_{}X'.format(args.output_prefix, target)
        else:
            prefix = '{}_{}X'.format(args.output_prefix, int(median_coverage))
        if n_reads > 0:
            write_bam(args.bam, prefix, region, target_reads['name'], keep_supplementary=args.keep_supplementary)
        coverage.fill(0.0)  # reset coverage for each target depth
        for read in target_reads:
            coverage[read['start'] - region.start:read['end'] - region.start] += 1
        _write_coverage(prefix, region, coverage, args.profile)

    return found_enough_depth


def subsample_region_uniformly(region, args):
    logger = logging.getLogger(region.ref_name)
    logger.info("Building interval tree.")
    tree = IntervalTree()
    with pysam.AlignmentFile(args.bam) as bam:
        ref_lengths = dict(zip(bam.references, bam.lengths))
        for r in bam.fetch(region.ref_name, region.start, region.end):
            if filter_read(r, args, logger):
                continue
            # trim reads to region
            tree.add(Interval(
                max(r.reference_start, region.start), min(r.reference_end, region.end),
                r.query_name))

    logger.info('Starting pileup.')
    coverage = np.zeros(region.end - region.start, dtype=np.uint16)
    reads = set()
    n_reads = 0
    iteration = 0
    it_no_change = 0
    last_depth = 0
    targets = iter(sorted(args.depth))
    target = next(targets)
    found_enough_depth = True
    while True:
        cursor = 0
        while cursor < ref_lengths[region.ref_name]:
            read = _nearest_overlapping_point(tree, cursor)
            if read is None:
                cursor += args.stride
                continue
            else:
                reads.add(read.data)
                cursor = read.end
                coverage[read.begin - region.start:read.end - region.start] += 1
                tree.remove(read)

        iteration += 1
        median_depth = np.median(coverage)
        stdv_depth = np.std(coverage)
        logger.debug(u'Iteration {}. reads: {}, depth: {:.0f}X (\u00B1{:.1f}).'.format(
            iteration, len(reads), median_depth, stdv_depth))
        # output when we hit a target
        if median_depth >= target or not found_enough_depth:
            if found_enough_depth:
                msg = "Hit target depth {}."
                logger.info(msg.format(target))
                prefix = '{}_{}X'.format(args.output_prefix, target)
                write_bam(args.bam, prefix, region, reads, keep_supplementary=args.keep_supplementary)
                _write_coverage(prefix, region, coverage, args.profile)
                try:
                    target = next(targets)
                except StopIteration:
                    break
            else:
                msg = "Target depth {} exceeds median coverage, limiting to {} and skipping higher depths."
                logger.warn(msg.format(target, int(median_depth)))
                prefix = '{}_{}X'.format(args.output_prefix, int(median_depth))
                if median_depth > 0:
                    write_bam(args.bam, prefix, region, reads, keep_supplementary=args.keep_supplementary)
                    _write_coverage(prefix, region, coverage, args.profile)
                break
        # exit if nothing happened this iteration
        if n_reads == len(reads):
            found_enough_depth = False
            if not args.force_low_depth:
                logger.warn("No reads added, finishing pileup.")
                break
        n_reads = len(reads)
        # or if no change in depth
        if median_depth == last_depth:
            it_no_change += 1
            if it_no_change == args.patience:
                found_enough_depth = False
                if not args.force_low_depth:
                    logging.warn("Coverage not increased for {} iterations, finishing pileup.".format(
                        args.patience
                    ))
                    break
        else:
            it_no_change == 0
        last_depth = median_depth
    return found_enough_depth


def _nearest_overlapping_point(src, point):
    """Find the interval with the closest start point to a given point.

    :param src: IntervalTree instance.
    :param point: query point.

    :returns: Interval instance of interval with closest start.

    """
    items = src.at(point)
    if len(items) == 0:
        return None
    items = sorted(items, key=lambda x: x.end - x.begin, reverse=True)
    items.sort(key=lambda x: abs(x.begin - point))
    return items[0]


def _write_coverage(prefix, region, coverage, profile):
    # depth profile
    output = '{}_{}.depth'.format(prefix, region.ref_name)
    end = profile * (len(coverage) // profile)
    cov_blocks = coverage[0:end].reshape(-1, profile)
    depth_profile = np.mean(cov_blocks, axis=1, dtype=np.uint32)
    start = region.start + profile // 2
    positions = (start + profile * x for x in range(len(depth_profile)))
    with open(output, 'w') as fh:
        fh.write("position\tdepth\n")
        for pos, depth in zip(positions, depth_profile):
            fh.write("{}\t{}\n".format(pos, depth))


if __name__ == '__main__':
    main()
