# 🧠 Semantic Tagging System – 模組功能與依賴結構

## 🔁 模型貼標流程

| 模組                     | 功能說明                           | 依賴                        |
|--------------------------|------------------------------------|-----------------------------|
| `extract_tags_fusion.py` | 兩模型貼標融合 (zh_embed + KeyBERT) | `SentenceTransformer`, `jieba` |
| `tag_cleaner.py`         | 停用詞 + 過渡詞 + 語意距離清洗      | `semantic_distance.py`, `opencc`, `yaml` |
| `semantic_distance.py`   | 計算 tag 與標題的語意相似度         | `sentence-transformers`, `sklearn` |

## 🧽 清洗與判定流程

| 模組                   | 功能說明                            |
|------------------------|-------------------------------------|
| `generate_highfreq_words.py` | 從語料中統計高頻詞                  |
| `generate_tfidf_scores.py`   | 詞的語意密度計算                    |
| `generate_pos_dict.py`       | 詞性標註                           |
| `update_generic_transitions.py` | 動態生成過渡詞清單（語意 + 詞性） |

## 🤖 語意審查與 LLM 路線

| 模組                 | 功能說明                                 |
|----------------------|------------------------------------------|
| `llm_reviewer.py`     | 實際呼叫 LLM 對標籤進行評估（內容語意判定） |
| `review2filter.py`    | 根據審查結果進行過濾                         |
| `analyze_tag_quality.py` | 記錄所有標籤清洗原因與語意得分               |

## 📊 報表與視覺化

| 模組                       | 功能說明                                   |
|----------------------------|--------------------------------------------|
| `tagging_report.py`         | 詞雲、分布分析                              |
| `similarity_heatmap.py`     | 標籤語意相似度視覺化                         |
| `semantic_review_log.py`    | 清洗原因追蹤紀錄（低分標籤、剃除統計等）         |

## 📤 匯出與整合

| 模組                     | 功能說明                          |
|--------------------------|-----------------------------------|
| `write_back_tags.py`      | 寫入 .md metadata                  |
| `generate_notion_import_csv.py` | 匯出為 Notion 相容格式              |

## 🧼 管理工具

| 模組           | 功能說明                |
|----------------|-------------------------|
| `semantic_pipeline.py` | 全流程自動化控制中心     |
| `clean.py`             | 清理中介與衍生產物         |
