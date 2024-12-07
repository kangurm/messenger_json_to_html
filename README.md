# messenger_json_to_html
Uses your **JSON** messenger history file to generate a presentable and easily readable file in **HTML** format.
### Contains two versions of the script:
<li>htmlmaker.py - clean infinitely scrollable html</li>
<li>htmlmaker-pages.py - divides document into multiple pages (still infinitely scrollable, but formatted for printing for example)</li><br>

# DISCLAIMER
This is by no means a polished or feature-rich program, this was made in a hurry for making the encrypted messenger json file visually pleasing and easy to read. Feel free to fork this if you want to improve and add features to it.

# HOW TO USE
1. Must have Python installed in your system to run the script.
2. Move the desired python script (htmlmaker.py or htmlmaker-pages.py) into same directory where you have **media** and the **JSON file** of the chat history.
3. **Rename the JSON file** you want to generate from to **messages.json** (or change variable in line 4 in code).
4. Run the script in that directory using a console (python command may vary) `python htmlmaker.py` or `python htmlmaker-pages.py`. Alternatively use python launcher.
