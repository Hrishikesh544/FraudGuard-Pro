#  FraudGuard Pro: Hybrid Financial Fraud Detection

**FraudGuard Pro** is an advanced financial security application that combines **Machine Learning behavioral analysis** with **Deterministic Business Rules**. While standard AI models can sometimes be overlooked by logical inconsistencies, this system utilizes a dual-layer approach to ensure absolute data integrity and catch sophisticated fraud patterns.

---

##  The Hybrid Advantage
Most fraud detection systems rely solely on AI, which can have "blind spots." FraudGuard Pro implements a **Defense-in-Depth** strategy:

* **Machine Learning Layer:** A **Random Forest Classifier** identifies subtle behavioral anomalies, such as sudden account drains or unusual high-velocity transfer patterns.
* **Deterministic Rule Layer:** Hard-coded forensic rules catch physical and logical impossibilities (e.g., spending more than the available balance) that a model might overlook.


---

##  Key Technical Features

* **Balance Error Engineering:** Developed custom features (`errorBalanceOrig` and `errorBalanceDest`) to audit mathematical discrepancies in real-time.
* **Risk Scoring:** Instead of a simple binary classification, the system provides a **Risk Probability Percentage**, allowing for tiered security responses.
* **Forensic Breakdown:** The UI provides a detailed explanation of *why* a transaction was flagged, citing specific rule violations or ML patterns.
* **Imbalance Handling:** Utilized `class_weight='balanced'` within the Random Forest algorithm to effectively train on highly imbalanced financial datasets.

---

##  Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python |
| **Modeling** | Scikit-Learn (Random Forest) |
| **Web Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Serialization** | Joblib |

---

##  Project Structure

```text
FraudGuard-Pro/
├── app.py                     # Streamlit User Interface & Hybrid Logic
├── train_model.py             # Model training & Feature Engineering script
├── improved_fraud_model.pkl   # The serialized Random Forest model
├── requirements.txt           # Project dependencies
└── fraud_data.csv             # Synthetic Financial Transaction Dataset
```


##  Example Test Scenarios
The system was validated against specific "stress test" cases to ensure the hybrid logic catches both behavioral and mathematical anomalies.

| Scenario | Logic Triggered | Expected Result | Reason |
| :--- | :--- | :--- | :--- |
| **Account Sweep** | **ML Pattern** |  **High Risk** | Recognizes intent to leave a balance of $0.00. |
| **Insufficient Funds**| **Rule A (Hard)** |  **High Risk** | Deterministic check: Amount exceeds available balance. |
| **Ghost Money** | **Rule B (Hard)** |  **High Risk** | Integrity check: Receiver got more than was sent. |
| **Small System Fee** | **ML + Tolerance**|  **Verified** | Allows for small discrepancies (up to 1%) common in banking. |
| **Wealthy User** | **Behavioral Context**|  **Verified** | Recognizes high-value transfers that leave healthy balances. |


---

##  Setup and Installation
Follow these steps to deploy the **FraudGuard Pro** environment on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Hrishikesh544/FraudGuard-Pro.git](https://github.com/Hrishikesh544/FraudGuard-Pro.git)
cd FraudGuard-Pro
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Generate the Model
```bash
python train_model.py
```
### 4. Launch the Dashboard
```bash
streamlit run app.py
```
