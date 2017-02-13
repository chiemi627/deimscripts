## DEIM 用のスクリプト
[![Build Status](https://travis-ci.org/chiemi627/deimscripts.svg?branch=master)](https://travis-ci.org/chiemi627/deimscripts)
### 実行環境
 * python 2.7.10 で実装＆動作確認をしています
 
### listSessions.py : セッションリスト（CSV）を出力する
 * セッション情報（セッション番号、セッション名、時間、座長等）をCSVファイル形式で出力します
 * 実行結果はPosTom（PosMAppのオーサリングサービス）のセッション情報ファイルとして使えます
 
 ```
 % python listSessions.py > sessions.csv
 ```

### listPresentations.py : 発表リスト（CSV）を出力する
 * プレゼン情報（発表番号、タイトル、概要、キーワード、著者等）をCSVファイルで出力します。
 * 実行結果はPosTomのプレゼンファイルとして使えます

 ```
 % python listPresentations.py > presen.csv
 ```

### listPresen4ReviewSheet.py : 発表リストの出力（評価シート用）
 * 評価シートの「発表者リスト」に入れるデータを生成します。
 
 ```
 % python listPresen4ReviewSheet.py > presen.csv
 ```

### generateVoteData : 電子集計データの整形
* 電子集計システム（PosVote）で出力された投票データ（PosVoteデータと呼びます）をvoteCheck.pyで使える投票データに整形します。
* PosVoteデータの他に参加者情報（参加者IDとtype,PosVoteIDの対応表）が必要です
* 入力ファイル（いずれも文字コードはutf-8でお願いします）
	* 参加者データ：(参加者ID,type,PosVoteID)が書かれたCSVファイル
		* type : 一般投票者は1, 座長・コメンテータは3
	* PosVoteデータ：(PosVoteID,[投票したポスターのID（１〜３件）)が書かれたCSVファイル
* 出力ファイル：投票データ。(参加者ID,type,ポスターID）が書かれたCSVファイル

```
% python generateVoteData.py participantdata.csv posvotedata.csv > votes.csv
```

### voteCheck.py : 投票チェック
 * インタラクティブセッションの投票数と投票者のリストを出力します。
 * 入力ファイル（いずれも文字コードはutf-8でお願いします）：
    * ポスターリスト：listPresen4ReviewSheet.py の出力ファイル
    * 参加者リスト：{参加者ID,姓,名,所属} が書かれたCSVファイル
    * 投票データ：{参加者ID,type,ポスターID}が書かれたCSVファイル
       * type : 一般投票者は1, 座長・コメンテータは3
 
 ```
 % python voteCheck.py posters.csv participants.csv votes.csv > result.csv
 ```
 * 結果はID,発表者,所属,タイトル,一般投票数,座長投票数,投票者一覧の順に出てきます。
 * 適当に集計・ソートしてください。

### generatePosterMap.py : ポスターマップ（SVGファイル）を作成する
 * PosMAppアプリのデータを使ってSVG形式のポスターマップを作ります
 * 印刷用，Webページ用にご活用ください

 ```
 % python generatePosterMap.py http://tkb-tsss.sakura.ne.jp/last/PosMapps/index/0UB9KVJ3 30 10
 ```
 * 第１引数はPosMAppのURLです
 * 第２, 第３引数はポスター一のoffsetです。背景とポスターの位置がずれることがあるのでこちらで調節してください。
 * day?.svgというファイルが生成されます。（２日間ポスターセッションがあれば、day1.svg, day2.svg）
