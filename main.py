import argparse

import NeatAI

import SearchAlgorithms


def main():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-t", "--Decision_Type",
                        help="Type of decisions for the Snake", type=str)

    parser.add_argument("-f", "--Genome_Name",
                        help="Name of the Genome", type=str)

    parser.add_argument("-m", "--Mode", help="Snake Mode", type=str)

    parser.add_argument("-v", "--Visualize",
                        help="Name of the Genome", type=str)

    # Read arguments from command line
    args = parser.parse_args()

    if args.Decision_Type == "a_star":
        SearchAlgorithms.GameSearch(10, 10, 10, 5).play()
        return
    if not args.Decision_Type == "neat":
        SearchAlgorithms.GameSearch(10, 10, 10, 5).play()
        return
    if args.Mode == "train":
        NeatAI.AI_Controller(10, 10, args.Visualize).train(
            args.Genome_Name, max_iter=200
        )

    if args.Mode == "play":
        NeatAI.AI_Controller(10, 10).play(args.Genome_Name)


if __name__ == "__main__":
    main()
