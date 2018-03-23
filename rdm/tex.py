import sys
import yaml
import subprocess


def yaml_gfm_to_tex(input_filename, output_file):
    with open(input_filename, 'r') as input_file:
        input_text = input_file.read()
    markdown, front_matter = extract_yaml_front_matter(input_text)
    validate_front_matter(front_matter)
    tex = convert_with_pandoc(markdown)
    tex_lines = tex.split('\n')

    add_margins(tex_lines)
    add_title_and_toc(tex_lines, front_matter)
    add_header_and_footer(tex_lines, front_matter)
    add_section_numbers(tex_lines)

    output_file.write('\n'.join(tex_lines))


expected_keys = {'category', 'id', 'revision', 'title', 'company_name'}


def validate_front_matter(front_matter):
    missing_keys = expected_keys - set(front_matter.keys())
    if len(missing_keys) > 0:
        msg = 'Missing required keys {} in the YAML front matter'
        raise ValueError(msg.format(",".join('"' + s + '"' for s in missing_keys)))


def extract_yaml_front_matter(raw_string):
    parts = raw_string.split('---\n')
    if len(parts) < 3:
        raise ValueError('Invalid YAML front matter')
    front_matter_string = parts[1]
    template_string = '---\n'.join(parts[2:])
    try:
        front_matter = yaml.load(front_matter_string)
    except yaml.YAMLError as e:
        raise ValueError('Invalid YAML front matter; improperly formatted YAML: {}'.format(e))
    return template_string, front_matter


def convert_with_pandoc(markdown):
    p = subprocess.run(
            ['pandoc', '-f', 'markdown_github', '-t', 'latex', '--standalone'],
        input=markdown,
        encoding='utf-8',
        stdout=subprocess.PIPE,
        universal_newlines=True
    )
    if p.returncode != 0:
        raise ValueError('Pandoc failed to convert markdown to latex')
    else:
        return p.stdout


def add_title_and_toc(tex_lines, front_matter):
    begin_document_index = tex_lines.index(r'\begin{document}')
    insert_lines(tex_lines, begin_document_index + 1, [
        r'\maketitle',
        r'\thispagestyle{empty}',
        r'\tableofcontents',
        r'\pagebreak',
    ])
    insert_lines(tex_lines, begin_document_index, [
        r'\title{' + front_matter['title'] + r' \\ ',
        r'\large ' + front_matter['id'] + ', Rev. ' + str(front_matter['revision']) + '}',
        r'\date{\today}',
        r'\author{' + front_matter['company_name'] + '}',
    ])


def add_header_and_footer(tex_lines, front_matter):
    begin_document_index = tex_lines.index(r'\begin{document}')
    insert_lines(tex_lines, begin_document_index + 1, [
        r'\thispagestyle{empty}',
    ])
    insert_lines(tex_lines, begin_document_index, [
        r'\usepackage{fancyhdr}',
        r'\usepackage{lastpage}',
        r'\pagestyle{fancy}',
        r'\lhead{' + front_matter['title'] + '}',
        r'\rhead{' + front_matter['id'] + ', Rev. ' + str(front_matter['revision']) + '}',
        r'\cfoot{Page \thepage\ of \pageref{LastPage}}',
    ])


def add_section_numbers(tex_lines):
    counter_index = tex_lines.index(r'\setcounter{secnumdepth}{0}')
    del tex_lines[counter_index]


def add_margins(tex_lines):
    tex_lines.insert(2, r'\usepackage[margin=1.25in]{geometry}')


def insert_lines(existing, index, new_lines):
    for line in reversed(new_lines):
        existing.insert(index, line)
