import re
from re import Match
import base64
import mimetypes
from pathlib import Path
import click
from typing import Union
from PIL import Image
from io import BytesIO

html_file = None
max_box_wh = (None, None)
max_box_wh = (1920, 1080)

def load_file(fname: str, box_resize= None, verb=True) -> str:
    '''Returns the text of a file and mime type
       If the file is binary, returns the encoded content
    '''
    global max_box_wh
    
    ### file exists & mime
    try:
        mime = mimetypes.guess_type(fname)[0]
    except:
        print(f'Error: file {fname} not found')
        exit()

    ### read content
    if mime.startswith('text/'):
        with open(fname, 'r') as f:
            out = f.read()
    else:
        # target size
        if box_resize == None:
            box_resize = max_box_wh
        with Image.open(fname) as img:
            size = img.size

        # resize needed?
        if size[0]>box_resize[0] or size[1]>box_resize[1]:
            # target dimensions
            scale_f = min(box_resize[0]/size[0], box_resize[1]/size[1])
            size_target = (int(scale_f * size[0]), int(scale_f * size[1]))
            # get out object resized
            with Image.open(fname) as img:
                with BytesIO() as buffer:
                    # resized in buffer
                    img.resize(size_target, Image.Resampling.LANCZOS).save(buffer, format="WEBP")
                    buffer.seek(0)
                    # encode
                    out = base64.b64encode(buffer.read())
                    out = f'data:{mime};base64,{out.decode("utf-8")}'
        # no resize
        else:
            with open(fname, 'rb') as f:
                out = base64.b64encode(f.read())
                out = f'data:{mime};base64,{out.decode("utf-8")}'

    ### verbose
    if verb:
        if mime=='text/html':
            tab = ''
        elif mime.startswith('text/'):
            tab = '  '
        else:
            tab = '    '

        try: 
            fname = fname.relative_to(html_file.parent.resolve())
            tab += '   '
        except:
            pass
        print(tab+str(fname))

    return out

def replace_html(m: Match) -> str:
    '''Replace function for html'''
    dic = m.groupdict()

    if dic['css'] is not None:
        return replace_css(dic)
    elif dic['script'] is not None:
        return replace_script(dic)
    elif dic['img'] is not None:
        return replace_img(dic)
    else:
        print('Error: bad pattern construction')
        print(m.re)
        print()
        exit(0)

def replace_css(d: dict) -> str:
    '''sub replace css'''
    # load file
    css_fname = html_file.parent / Path(d['fname_css'])
    css = load_file(css_fname)

    # replace img
    url_pattern = r'image:\s*url\(\s*["\']?(?P<fname_css_img>[^"\')]+)["\']?\s*\)'
    css = re.sub(url_pattern, 
                 lambda match: replace_css_img(match, css_fname.parent), 
                 css,
                 flags=re.IGNORECASE)

    # output replacement
    out = f"\n<!-- {d['fname_css']} -->\n"
    out += "<style>\n"
    out += css
    out += "\n</style>\n"

    return out

def replace_script(d: dict) -> str:
    '''sub replace script'''
    fname = html_file.parent / Path(d['fname_script'])

    out = f"\n<!-- {d['fname_script']} -->\n"
    out += "<script>\n"
    out += load_file(fname)
    out += "\n</script>\n"

    return out

def replace_img(d: dict) -> str:
    src = d['fname_img']
    if 'data:image' in src or src.startswith('https://'):
        return d['img']

    fname = html_file.parent / Path(d['fname_img'])
    src_pattern = r'\s+src\s*=\s*["\'](?P<fname_img>[^"\']+)["\']'
    out  = "\n"
    out += re.sub(src_pattern, 
                  f' src={load_file(fname)} ', 
                  d['img'],
                  flags=re.IGNORECASE)
    out += '\n'
    
    return out

def replace_css_img(m: Match, base_path: Path) -> str:
    fname = (base_path / Path(m['fname_css_img'])).resolve()
    return f"image: url('{load_file(fname)}')"

@click.command()
@click.argument('fname', 
                type=click.Path(exists=True),
                required = True)
def package(fname: Union[str, Path]) -> None:
    global html_file
    html_file = Path(str(fname))

    css_pattern = r'(?P<css><\s*link\b[^>]*rel\s*=\s*["\']stylesheet["\'][^>]*href\s*=\s*["\'](?P<fname_css>[^"\']+)["\'][^>]*>)'
    script_pattern = r'(?P<script><\s*script\b[^>]*src\s*=\s*["\'](?P<fname_script>[^"\']+)["\'][^>]*>\s*</script>)'
    img_pattern = r'(?P<img>(<\s*img\b[^>]*src\s*=\s*["\'])(?P<fname_img>[^"\']+)(["\'][^>]*>))'
    pattern = css_pattern
    pattern = script_pattern
    pattern = '|'.join([css_pattern, script_pattern, img_pattern])

    html = load_file(fname)

    out = re.sub(pattern, replace_html, html, flags=re.IGNORECASE)

    oufname = html_file.with_stem(html_file.stem + '_pkg')
    with open(oufname, 'w') as f:
        f.write(out)
    print(f'Packaged HTML saved as {oufname}')


if __name__ == '__main__':
    package()
