主なライブラリ
NFC読み書き(nfcpy)&GUI作成(tkinter)&常駐アプリ化(pystray)&通知処理(pyler)&exe化(pyinstaller)

内容
CSV: 空のユーザーリスト、ログデータ
ICON: 通知、アプリケーションのico画像(好きな画像に変更可)
/dist/Attendance: アプリケーション(exe)
exeファイルと同じ階層にCSV,ICONの２つのファイルを置くこと

実行
(1) NFCの読み取り準備 ドライバ等
(2) 実行アプリ化用仮想環境作成(requirementが最低限必要)
(3) 環境下でpyinstaller Attendance.spec でexe化
(4) exeのショートカットを作成、スタートアップアプリに追加
＝常駐アプリ

参考文献：
https://www.kosh.dev/article/3/

https://wp.utopiat.net/2017/05/171/

https://gist.github.com/watagashi0619/639062958adbc60f44e6c3f8fdb79a74

https://tech-blog.cloud-config.jp/2019-04-27-new-hire-training-windows-nfcpy/

https://wazalabo.com/python-script.html

https://qiita.com/firedfly/items/f6de5cfb446da4b53eeb