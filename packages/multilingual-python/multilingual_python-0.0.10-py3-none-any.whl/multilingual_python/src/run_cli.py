from pre_process import PreProcessor

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Multilingual Python Preprocessor")
    parser.add_argument('command', choices=['translate', 'run', 'run_direct', 'translate_dir', 'run_dir'], help="Action to perform.")
    parser.add_argument('input_path', help="Input file or directory to process.")
    parser.add_argument('-o', '--output', default='translated.py', help="Output file or directory for the translated Python code.")
    parser.add_argument('-l', '--language', default='lang_map_json/hindi_to_english.json', help="Language mapping file (JSON).")
    parser.add_argument('-m', '--main', help="Main file to execute when running a directory.")

    args = parser.parse_args()

    preprocessor = PreProcessor(args.language)

    if args.command == 'translate':
        preprocessor.translate_file(args.input_path, args.output)
        print(f"Translated file saved to {args.output}")

    elif args.command == 'run':
        preprocessor.translate_file(args.input_path, args.output)
        print(f"Running translated code from {args.output}...")
        preprocessor.execute_translated_code(open(args.output).read())

    elif args.command == 'run_direct':
        print("Running code directly after translation...")
        preprocessor.execute_file_directly(args.input_path)

    elif args.command == 'translate_dir':
        preprocessor.translate_directory(args.input_path, args.output)
        print(f"Translated directory saved to {args.output}")

    elif args.command == 'run_dir':
        if not args.main:
            raise ValueError("Main file must be specified when running a directory.")
        print(f"Translating directory '{args.input_path}' and executing main file '{args.main}'...")
        preprocessor.execute_directory(args.input_path, args.main)
