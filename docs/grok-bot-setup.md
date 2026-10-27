# Grok Bot 怎麼建組織

這裡只寫已知做得到的事，以及會踩到的限制。沒有列出來的功能，不要假設產品有。

主 bot 負責建立。其他 bot 有沒有同樣的工具，不知道，不要假設。

## 建立 bot

用 CreateAgent。給名字，再給一段 description，當作這隻 bot 的個人簡介。

個人簡介放不下長文。字數上限不知道。長簡述放私人記憶庫，簡介保持短，並寫明記憶庫的位置。模板：

- [../templates/lead-brief.md](../templates/lead-brief.md)
- [../templates/coordinator-brief.md](../templates/coordinator-brief.md)

使用者同意計畫之前，不呼叫 CreateAgent。

主 bot 不能刪 bot。建錯了，請使用者從側邊欄刪，再改私人名單。所以不要先建一堆備用。

## 建立會議室

用 CreateChannel 開群組。名稱在建立時定死，不能改名。

改成員用 UpdateChannel。加人、移出都走這個。人滿了要換人，先移再加。

一個頻道最多 6 人，含主 bot。bot 在頻道裡的每一則回覆，都算使用者的每週額度。成員沒被點名就不要說話。房間怎麼配，見 [operating-rules.md](operating-rules.md)。

能不能刪頻道，不知道。名稱要在建立前定好。想改名，就開一個新的，舊的怎麼處理問使用者。

## 跟 bot 說話

用 SendToAgent。它是非同步的。

- `priority: true`：叫醒對方
- `priority: false`：只把訊息留著，等對方下一次自己開工。不會為了這則訊息把對方叫醒

回覆晚點才到，不是這一次呼叫立刻拿到。送出後繼續做別的事，回覆來了再處理。不要把沒回覆當成拒絕或同意。

bot 在別人告訴它之前，不知道其他 bot 的 id。建立之後，把名字和 id 寫進私人記憶庫的名單，並告訴它向誰回報。id 只放私人名單。

## 改程式

repo 上的程式交給 cloud coding agent（CloudAgent）。在分支上做，用 PR 交付。

主管不自己 clone，也不自己 merge。commit、push、打包仍是三件分開的事，每一件都要使用者或主 bot 明確同意。CloudAgent 還有哪些參數，這裡沒有寫，不要自己補。

## 私人記憶庫

使用者開一個 private GitHub repo。主 bot 目前不能自己建 repo，有授權也不行。訪談第 7 題要使用者開好並授權。

每個 bot 開工前先讀它。bot 會因為摘要或新對話丟掉上下文，所以組織資料放那裡，不放在這份公開框架裡。

## 同一台電腦

這些 bot 共用一個檔案系統。對話和記憶分開，檔案不會跟著分開。秘密不要寫進共享檔案。保密靠規則：不把金鑰、憑證放進對話、提交、日誌或共享路徑。

## 主管底下的團隊檔

一個主管如果還需要專案裡的小團隊檔案，參考 A-Team 的 `grok-native` 分支。那個分支會產出團隊：小專案用精簡流程（small office），大約 3 到 4 個階段、3 到 5 位專員，一個階段一份紀錄；大專案用完整流程。分支裡的監督文件有八行回報的一種寫法。本框架主管向上用的八行，以 [operating-rules.md](operating-rules.md) 為準。內容留在那個 repo，不抄進這份框架。

https://github.com/chemistrywow31/A-Team/tree/chemistrywow31/grok-native

## 容易踩到的點

- 簡介寫太長。長文進記憶庫，簡介只留身份、回報對象、記憶庫連結。
- 頻道名稱建完不能改。
- SendToAgent 不會在同一輪帶回回覆。`priority: false` 不會叫醒對方。
- 建多的 bot 要使用者自己從側邊欄刪。
- 新 bot 不知道別人的 id，名單沒寫就會傳錯人或傳不到。
- 共享資料夾不是私人抽屜。
- 記憶庫沒開、或主 bot 打不開，就先不要建 bot。
- 看回報不是在做那個專案的測試。
- 一句「去做」不會同時授權 commit、push、打包。
