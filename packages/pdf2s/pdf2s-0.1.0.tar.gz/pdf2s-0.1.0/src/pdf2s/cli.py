import argparse
from .converters import pdf_merger, md_pdf, pdf_md, pdf_splitter


def main():
    parser = argparse.ArgumentParser(
        prog="pdf2s",
        description="PDF Manipulation Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge PDF files')
    merge_parser.add_argument('directory', help='Source directory with PDFs')
    merge_parser.add_argument('output', help='Output PDF file name')
    merge_parser.add_argument(
        '--regex',
        '-r',
        help='Regex pattern to filter filenames')
    merge_parser.add_argument(
        '--sort',
        action='store_true',
        help='Sort files alphabetically')

    # MD to PDF command
    md_parser = subparsers.add_parser('md2pdf', help='Convert Markdown to PDF')
    md_parser.add_argument('input', help='Input Markdown file')
    md_parser.add_argument('output', help='Output PDF file')
    md_parser.add_argument(
        '--style',
        '-s',
        help='CSS style sheet for formatting')

    # PDF to MD command
    pdfmd_parser = subparsers.add_parser(
        'pdf2md', help='Convert PDF to Markdown')
    pdfmd_parser.add_argument('input', help='Input PDF file')
    pdfmd_parser.add_argument('output', help='Output Markdown file')

    # Split command with improved arguments
    split_parser = subparsers.add_parser('split', help='Split PDF files')
    split_parser.add_argument('input', help='Input PDF file')
    split_parser.add_argument('output_dir', help='Output directory')
    split_group = split_parser.add_mutually_exclusive_group()
    split_group.add_argument('--pages', type=int, default=1,
                             help='Split every X pages (default: 1)')
    split_group.add_argument(
        '--ranges',
        help='Page ranges (e.g., "1-3,4-6" or "all")')

    args = parser.parse_args()

    try:
        if args.command == 'merge':
            pdf_merger.merge_pdfs(
                args.directory,
                args.output,
                args.regex,
                args.sort)
        elif args.command == 'split':
            pdf_splitter.split_pdf(
                args.input,
                args.output_dir,
                args.pages,
                args.ranges)
        elif args.command == 'md2pdf':
            md_pdf.convert_md_to_pdf(args.input, args.output, args.style)
        elif args.command == 'pdf2md':
            pdf_md.convert_pdf_to_md(args.input, args.output)
        print("Operation completed successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
