#!/usr/bin/env python3
# file.py

""" ファイル
ファイル操作サンプル集
"""

from console import *
import os,shelve, shutil

def makedir(path):
    ''' ディレクトリ作成
    '''
    try:
        os.makedirs(path)
    except FileExistsError as error:
        # 既にフォルダが存在する場合はそのまま処理をすすめる
        log('DO NOT MAKE DIR. ALREADY EXISTS : {0}'.format(path))
    else:
        log('COMPLETE MAKE DIR : {0}'.format(path))

def remove(path):
    '''ファイル/ディレクトリ一括削除
    '''
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
            # 下記でも同等の挙動
            #os.unlink(path)
    except FileNotFoundError as error:
        log('NOT EXISTS : {0}'.format(path))
    else:
        log('COMPLETE REMOVE : {0}'.format(path))

def read_file(file_path, isDebug=True):
    '''ファイル読込
    '''
    # openでFileオブジェクト取得
    # readで内容読込
    # closeでファイルを閉じる
    file = None
    try:
        # r指定で読み取り専用として開く
        file = open(file_path, 'r')
        content = file.read()
        log('READ', file_path, content)
    except Exception as ex:
        log('ERROR', ex)
    finally:
        if file != None:
            file.close()

def readline_file(file_path, isDebug=True):
    '''ファイル１行毎読込
    '''
    log('READ', file_path)
    # withでopenすることでclose漏れがなくなる
    with open(file_path) as file:
        line = file.readline()
        lineCount = 0
        while line:
            lineCount = lineCount + 1
            if isDebug:
                log('LINE({0})'.format(str(lineCount)), remove_line_separator(line))
            line = file.readline()

def readlines_file(file_path, isDebug=True):
    '''ファイル全行読込
    '''
    with open(file_path) as file:
        lines = file.readlines()
        if isDebug:
            log('READ LINES', lines)
    
def write_file(file_path, mode, contennt=''):
    ''' ファイル書込
    '''
    with open(file_path, mode) as file:
        writeNum = file.write(contennt)
        log('WRITE FILE', 'Write Character', writeNum)
        # 書き込んだ内容表示
        readline_file(file_path)

def make_file(file_path, mode='w'):
    '''ファイル作成
    '''
    file = None
    try:
        file = open(file_path, mode)
    except Exception as ex:
        log('ERROR', ex)
    return file;

def save_shelve(key, value):
    shelve_file = shelve.open('temp_data')
    shelve_file[key] = value
    shelve_file.close()
    log('save shelve')

def get_shelve(key):
    shelve_file = shelve.open('temp_data')
    value = shelve_file[key]
    shelve_file.close()
    log('get shelve')
    return value

def remove_line_separator(line):
    _line = str(line)
    # 3項演算子
    return _line.strip('\n').strip('\r') if line != None else line;


def main():
    log('#============================')
    log('# ファイル操作')
    log('#============================')
    # 基本 +++++++++++++++++++++++
    # フォルダの区切りはOS毎に異なる。両方に対応するよう実装するには、os.path.joinを利用することで実現可能
    # Windows : \
    # Linux, Mac : /
    log('> osパッケージ基本')
    log(' - ディレクトリ表示、ディレクトリ移動')
    log('PATH', os.path.join('usr', 'bin', 'span'))
    log('CURRENT DIR', os.getcwd())
    # ユーザのホームディレクトリ
    home_dir = os.path.expanduser('~')
    log('HOME DIR', home_dir)
    log_add_line(1)
    # 場所移動
    dir_script = os.path.abspath(__file__)
    os.chdir(home_dir)
    log('CHANGE DIRECTORY -> ' + home_dir) 
    log('CURRENT DIR', os.getcwd())

    # ディレクトリ作成
    # 中間ディレクトリも作成される
    # os.mkdirも新規ディレクトリ作成可能だが、既存ディレクトリに対しての追加しかできない。
    # 中間ディレクトリ毎一括で作成するにはos.makedirsを使うのがよい
    log(' - ディレクトリ作成')
    work_dir = os.path.join(home_dir, 'work_python')
    # 一度ワークディレクトリ削除
    remove(work_dir)
    worK_dir_test_makedir = os.path.join(work_dir, 'makedirs_test')
    makedir(worK_dir_test_makedir)
    log('WORK DIR', worK_dir_test_makedir)
    os.chdir(worK_dir_test_makedir)
    log_add_line(1)

    log(' - パス判定')
    log('GET ABSOLUTE PATH', os.path.abspath('.'))
    log('IS ABSOLUTE PATH(.)', os.path.isabs('.'))
    log('IS ABSOLUTE PATH(/)', os.path.isabs('/'))
    # 第２引数（home_dir）から、第１引数（ルードディレクトリ）への相対パスを表現`
    log('GET RELATIVE PATH', os.path.relpath('/', home_dir)) 
    log_add_line(1)

    log(' - その他')
    log('GET BASENAME', os.path.basename(worK_dir_test_makedir))
    # 指定した末尾のディレクトリ、ファイル名を取得
    log('GET DIRNAME', os.path.dirname(worK_dir_test_makedir))
    # basenameまでのパスと分けて取得したい場合はsplitで取得可能（タプル）
    log('SPLIT', os.path.split(worK_dir_test_makedir))
    # ファイル/ディレクトリサイズ確認（byte）
    log('SIZE', os.path.getsize(worK_dir_test_makedir), 'byte')
    # 指定したパス以下のディレクトリ、ファイルの一覧を取得可能
    log('LIST DIR/FILE', os.listdir(home_dir))
    # ファイルパス存在確認
    log('EXISTS PATH', os.path.exists(worK_dir_test_makedir))
    # ファイル確認
    log('IS FILE', os.path.isfile(worK_dir_test_makedir))
    # ディレクトリ確認
    log('IS DIR', os.path.isdir(worK_dir_test_makedir))
    log_add_line()


    # ファイル読込／書込 +++++++++++++++++++++++
    log('>ファイル読込／書き込み')
    file_path_test_dir = os.path.join(work_dir, 'file_test')
    makedir(file_path_test_dir)
    file_path_test = os.path.join(file_path_test_dir, 'TEST.txt')


    # ファイル書込
    # w：書込（新規）
    # a：書込（追記）
    log(' - write(w)')
    write_file(file_path_test, 'w', 'write file w mode\nnew line\n')
    log_add_line(1)
    log(' - write(a)')
    write_file(file_path_test, 'a', 'write file a mode\nadd line\nadd line\n')
    log_add_line(1)


    # ファイル読込
    log(' - read')
    read_file(file_path_test)
    log(' - readline')
    readline_file(file_path_test)
    log(' - readlines')
    readlines_file(file_path_test)
    log_add_line(1)


    # shelve（シェルフ：棚） +++++++++++++++++++++++
    # バイナリファイルとして一時的に保存が可能
    # shelveパッケージをインポートして利用する
    log(' - shelve')
    save_shelve('condition', {'key1' : 1, 'key2' : 10})
    condition = get_shelve('condition')
    log('SHELVE', condition)
    log_add_line()


    # pprint.pformat +++++++++++++++++++++++
    # Pythonでそのまま利用できる形でファイル保存が可能
    log(' - pprint.pformat -> file')
    import pprint
    sample_data = [{'key1' : 'value1'}, {'key2' : 'value2', 'key3' : 'value3'}]
    # 後にimportするため、change directoryする前のスクリプト実行ディレクトリに配置する
    content_formated = 'sample_data_formatted = ' + pprint.pformat(sample_data) + ';\n'
    log('PPRINT.PFORMAT', content_formated)
    # このファイルを後ほどimportする
    filepath_format_test = os.path.dirname(dir_script) + '/pprintTest.py'
    write_file(filepath_format_test, 'w', content_formated)
    log('import pprint.pformat file')
    import pprintTest
    sample_data_formatted = pprintTest.sample_data_formatted
    log('AFTER IMPORT(ALL)', sample_data_formatted, title_space=20)
    log('AFTER IMPORT(0)', sample_data_formatted[0], title_space=20)
    log('AFTER IMPORT(0)', sample_data_formatted[1], title_space=20)
    log_add_line()

if __name__ == '__main__':
    main()
