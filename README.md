# JSON Token Optimizer  

**Optimize JSON data for efficient LLM ingestion by reducing token count.**  

This repository provides a utility to optimize JSON input by minifying its structure, truncating timestamps, abbreviating large numbers, and optionally stripping unnecessary quotation marks. The goal is to reduce the token count when sending data to an LLM (Large Language Model), improving efficiency and cost-effectiveness.  

## Features  

✅ **JSON Minification** – Removes unnecessary spaces and compresses JSON structure.  
✅ **Timestamp Truncation** – Shortens ISO 8601 timestamps to reduce token usage (minute, hour, date, or month).  
✅ **Number Abbreviation** – Converts large numbers into shorter formats (e.g., `1200000` → `1.2M`).  
✅ **Quote Stripping** – Optionally removes quotes around strings to save additional tokens.  
✅ **Custom Replacements** – Replace specific text values within the JSON.  

## Installation  

Clone the repository and install dependencies if needed (only standard library is used).  

```bash
git clone https://github.com/your-username/json-token-optimizer.git
cd json-token-optimizer
```

## Usage  

### Example: Optimize a JSON file  

```python
import json
from json_token_optimizer import JsonTokenOptimizerBase  # Assuming you rename the script accordingly

with open("ecommerce.json") as f:
    data = json.load(f)
    optimized_json = (
        JsonTokenOptimizerBase(data)
        .strip_quotes()  
        .abbreviate_numbers()
        .truc_timestamp(level="minute")
        .output()
    )
    print(optimized_json)
```

### Available Methods  

- `strip_quotes()`: Removes unnecessary double quotes from strings.  
- `truc_timestamp(level="minute")`: Truncates timestamps to **minute, hour, date, or month** level.  
- `abbreviate_numbers()`: Converts large numbers (e.g., `7500` → `7.5K`, `1200000` → `1.2M`).  
- `replace(old, new)`: Replace a substring with a new value.  
- `output()`: Returns the optimized JSON string.  

### Example JSON Optimization  

#### **Input JSON**  

```json
{
    "product": "Smartphone",
    "price": 1200000,
    "stock": 7500,
    "last_updated": "2024-03-05T14:23:56Z"
}
```

#### **Optimized Output**  

```json
{
    product:Smartphone,
    price:1.2M,
    stock:7.5K,
    last_updated:2024-03-05T14:23
}
```

## Contributions  

Feel free to open issues, suggest optimizations, or submit PRs to improve the efficiency of JSON compression further.  

## License  

This project is licensed under the MIT License.

