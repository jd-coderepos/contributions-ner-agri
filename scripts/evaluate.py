from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()

    parser.add_argument('-testf', '--test_file',
                        type=str,
                        required=False,
                        help='Path to the test data file for evaluation in CONLL2003 format.'
                        )

    parser.add_argument('-predictf', '--predictions_file',
                        type=str,
                        required=False,
                        help='Path to the predictions data file for evaluation in CONLL2003 format.'
                        )

    parser.add_argument('-tagf', '--tag_format',
                        type=str,
                        required=False,
                        help='IOB or IOBES',
                        default='IOB')

    return parser.parse_args()

def main():
    args = config or parse_args()

    assert args.testf, 'test file must be provided.'
    assert args.predictf, 'predictions file must be provided.'
    assert args.tagf, 'tag format for evaluations must be provided'

    if args.tagf == 'IOB':
        evaluate-IOB.evaluate(args.predictf, args.testf)
    elif args.tagf == 'IOBES':
        evaluate-IOBES.evaluate(args.predictf, args.testf)
        

if __name__ == '__main__':
    main()