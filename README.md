# 🎮 Number Guessing Game — Python Edition

A fun, logic-based **command-line game** built with **Python**, designed to sharpen your **analytical thinking** and **decision-making** skills.

Players must guess a secret number within a given range — guided by smart hints, progressive difficulty, and a reward-based scoring system.  



## 🚀 Features

✅ **Multiple Levels** — Start small and progress to higher ranges as difficulty increases.  
✅ **Hint Shop System** — Buy clues like parity, range elimination, or digit sum using your points.  
✅ **Colorful CLI Interface** — Clean, modern look using `colorama` for colorized feedback.  
✅ **High Score Tracking** — Automatically saves your best scores in `data/highscores.json`.  
✅ **Smart Scoring System** — Points deducted for wrong guesses, rewards for accuracy.  
✅ **Fully Modular Code** — Built with separate modules for logic, scoring, and UI.  



## 🧠 Game Objective

Your goal is simple:  
> Guess the correct number in the fewest attempts possible  
> while keeping your score above zero.

Use logical reasoning and the hint shop strategically — every decision affects your score!


## 🖥️ Gameplay Preview

| Gameplay | Hint Shop | High Scores |
|:--:|:--:|:--:|
| ![Gameplay Screenshot](screenshots/gameplay.png) | ![Hint Shop Screenshot](screenshots/hintshop.png) | ![High Score Screenshot](screenshots/highscores.png) |

*(Screenshots from actual gameplay)*



## ⚙️ Tech Stack

- **Language:** Python  
- **Libraries:** `colorama`, `random`, `json`, `dataclasses`  
- **Paradigm:** Object-Oriented Programming  
- **Persistence:** JSON-based local storage  

## 🗂️ Project Structure
number-guess/
├── game/
│   ├── __init__.py
│   ├── main.py               
│   ├── core.py               
│   ├── score.py              
│   └── utils.py              
├── data/
│   └── highscores.json      
├── tests/
│   └── test_core.py
├── README.md
├── requirements.txt
└── .gitignore


🏆 **Example Hints Available**

 Hint                    Description                                    Cost   
 ------------------      ------------------------------------------     ------ 
 🔢 Parity               Reveals if the number is even or odd           5 pts  
 🎯 Within ±10           Tells if target is within 10 of an anchor      8 pts  
 🚫 Eliminate Third      Removes a third of the range                   12 pts 
 🧮 Digit Sum            Shows sum of digits of target                  7 pts  


📈 **Scoring System**

 Action               Effect                                     
 ---------------      ------------------------------------------ 
 ✅ Correct Guess     Bonus points (fewer attempts → more bonus) 
 ❌ Wrong Guess       -X points (based on range)                 
 💡 Buying Hint        Deducts hint cost from score               
 🏁 Score ≤ 0         Game Over                                  

💡 **Why This Project Matters**

This project goes beyond a simple number-guessing app — it’s designed to:
 - Strengthen logical reasoning
 - Reinforce decision-making under constraints
 - Demonstrate clean, modular Python coding


🌟 **Connect**

If you like this project, feel free to:

⭐ Star the repo

🐛 Open an issue or suggest a feature

💬 Connect on LinkedIn - http://www.linkedin.com/in/vasitha
