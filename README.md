針對 **`adv-01-unit-jpeg-quality` (影像品質參數的權衡)** 單元，這是一個涉及「嵌入式運算」、「網路傳輸」與「電腦視覺演算法」三者交集的進階課題。

以下是在 **GitHub Classroom** 部署其作業 (Assignments) 的具體建議：

### 1. 範本倉庫 (Template Repo) 配置建議
進階單元的範本應更具「工具化」，建議包含：
*   **📂 `firmware/`**：提供 ESP32-CAM 韌體，需包含一個可透過 REST API 動態修改 `config.jpeg_quality` 的介面。
*   **📂 `analysis/results.csv`**：預置一個效能對照表，讓學員填入不同 Q 值下的 $FPS$ 與 $KB/Frame$ 數據。
*   **📂 `web/vision-core.js`**：核心視覺處理腳本，將質心計算 (Centroid) 與品質切換邏輯留給學員實作。
*   **📂 `.github/workflows/grading.yml`**：設置自動化檢查，驗證學員是否有按時回傳實驗數據。

---

### 2. 作業任務部署細節

#### 任務 1：品質、大小與 FPS 關聯標定 (Scaling Lab)
*   **目標**：量化影像品質對通訊頻寬的具體影響，尋找傳輸「拐點」。
*   **Classroom 部署建議**：
    *   **自動化評分 (Autograding)**：檢查 `analysis/results.csv` 是否已被正確填充且符合「品質上升 -> 大小上升 -> FPS 下降」的物理規律。
    *   **挑戰項**：要求學員在 README 中標出「邊際效益遞減」的 Q 值點（通常在 80 以上檔案激增但畫質提升有限）。

#### 任務 2：演算法抗噪測試 (Centroid Jitter Lab)
*   **目標**：觀察 JPEG 「方塊效應」對影像邊緣偵測的干擾。
*   **Classroom 部署建議**：
    *   **驗證方式**：學員需在 README 中上傳兩張對比圖：一張是 Q=90 時穩定的質心標記，另一張是 Q=10 時質心因雜訊產生的「座標跳動 (Jitter)」。
    *   **數據提交**：要求學員將 100 幀內的質心 X 座標偏差值存入 `jitter-log.json` 並上傳。導師核閱其偏差值是否在低畫質下顯著增加。

#### 任務 3：動態品質切換策略 (Adaptive Strategy)
*   **目標**：開發「情境感知」的畫質切換邏輯。
*   **Classroom 部署建議**：
    *   **邏輯檢核**：
        ```javascript
        // 核心邏輯：靜態細節優先，動態流暢優先
        if (motorSpeed === 0) setQuality(80); 
        else setQuality(20);
        ```
    *   **驗證方式**：導師在 PR 中核對此條件判斷是否正確實作，並確認學員是否考慮了切換時的「抖動保護 (Debounce)」，防止畫質頻繁閃爍。

---

### 3. 進階單元導師點評標準 (Advanced Benchmarks)
此階段評分應側重於 **「工程數據的詮釋能力」**：
*   [ ] **數據敏感度**：學員是否能解釋為什麼 10 Mbps 的網路在 Q=90 時會導致影像嚴重延遲？
*   [ ] **雜訊處理思維**：面對 Q=10 的馬賽克，學員是否提出使用「模糊濾波 (Blur)」來減少假邊緣？
*   [ ] **系統整合度**：動態切換策略是否能與馬達控制信號無縫同步？

### 📁 推薦範本結構 (GitHub Classroom Template)：
```text
.
├── firmware/              # ESP32 韌體 (支援動態 Q 值 API)
├── web/                   
│   └── vision-logic.js    # 學員實作質心與動態切換處
├── analysis/              
│   ├── results.csv        # 效能採集數據表
│   └── jitter-log.json    # 質心座標穩定性紀錄
└── README.md              # 影像實驗報告 (含數據圖表)
```

透過這種部署方式，學生能切身體會到 **「沒有最好的參數，只有最適合場景的權衡」**。這對於培養解決真實世界複雜問題的架構思維極有幫助。
