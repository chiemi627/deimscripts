# DEIM 用のスクリプト
## listSessions.py : セッションリスト（CSV）を出力する
 * セッション情報（セッション番号、セッション名、時間、座長等）をCSVファイル形式で出力します
 * 実行結果はPosTom（PosMAppのオーサリングサービス）のセッション情報ファイルとして使えます
 
 ```
 % python listSessions.py > sessions.csv
 ```

## listPresentations.py : 発表リスト（CSV）を出力する
 * プレゼン情報（発表番号、タイトル、概要、キーワード、著者等）をCSVファイルで出力します。
 * 実行結果はPosTomのプレゼンファイルとして使えます

 ```
 % python listPresentations.py > presen.csv
 ```

## listPresen4ReviewSheet.py : 発表リストの出力（評価シート用）
 * 評価シートの「発表者リスト」に入れるデータを生成します。
 ```
 % python listPresen4ReviewSheet.py > presen.csv
 ```

