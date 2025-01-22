1. **`switch_case(variable, cases)`**
   - **`variable`**: A value to check against the dictionary `cases`.
   - **`cases`**: A dictionary where keys are the possible values of `variable` and values are the corresponding functions to execute.
   - **What it does**: Mimics a switch-case statement, executing the function associated with the value of `variable`.

2. **`pop(message)`**
   - **`message`**: A string to display in a message box.
   - **What it does**: Displays a simple message in a pop-up window.

3. **`popinp(message)`**
   - **`message`**: A string to display in an input dialog.
   - **What it does**: Prompts the user for input through a dialog box.

4. **`main_window()`**
   - **What it does**: Use it as a root like root = main_window().

5. **`set_window_size(width, height)`**
   - **`width`**: The desired width of the window.
   - **`height`**: The desired height of the window.
   - **What it does**: Sets the size of the window.

6. **`center_window(window, width, height)`**
   - **`window`**: The Tkinter window object.
   - **`width`**: The width of the window.
   - **`height`**: The height of the window.
   - **What it does**: Centers the window on the screen.

7. **`minimize_window(window)`**
   - **`window`**: The Tkinter window object.
   - **What it does**: Minimizes the window.

8. **`maximize_window(window)`**
   - **`window`**: The Tkinter window object.
   - **What it does**: Maximizes the window.

9. **`set_window_bg_color(window, color)`**
   - **`window`**: The Tkinter window object.
   - **`color`**: A string representing the color to set as the background (e.g., `"red"`, `"blue"`).
   - **What it does**: Sets the background color of the window.

10. **`create_button(window, text, command)`**
    - **`window`**: The Tkinter window object.
    - **`text`**: The label or text to display on the button.
    - **`command`**: The function to call when the button is clicked.
    - **What it does**: Creates a button widget.

11. **`create_label(window, text)`**
    - **`window`**: The Tkinter window object.
    - **`text`**: The text to display on the label.
    - **What it does**: Creates a label widget.

12. **`create_text_widget(window, height, width)`**
    - **`window`**: The Tkinter window object.
    - **`height`**: The height of the text widget.
    - **`width`**: The width of the text widget.
    - **What it does**: Creates a text widget for multi-line text input.

13. **`bind_mouse_click(widget, callback)`**
    - **`widget`**: The Tkinter widget to bind the mouse click event to.
    - **`callback`**: The function to call when the mouse click happens.
    - **What it does**: Binds a mouse click event to a widget.

14. **`bind_key_press(widget, callback)`**
    - **`widget`**: The Tkinter widget to bind the key press event to.
    - **`callback`**: The function to call when a key is pressed.
    - **What it does**: Binds a key press event to a widget.

15. **`move_file(src, dest)`**
    - **`src`**: The source file path.
    - **`dest`**: The destination file path.
    - **What it does**: Moves a file from `src` to `dest`.

16. **`copy_file(src, dest)`**
    - **`src`**: The source file path.
    - **`dest`**: The destination file path.
    - **What it does**: Copies a file from `src` to `dest`.

17. **`create_directory(path)`**
    - **`path`**: The directory path to create.
    - **What it does**: Creates a new directory at the specified `path`.

18. **`create_zip_file(file_paths, zip_path)`**
    - **`file_paths`**: A list of paths to files to include in the ZIP.
    - **`zip_path`**: The path where the resulting ZIP file should be saved.
    - **What it does**: Creates a ZIP file from the specified files.

19. **`extract_zip_file(zip_path, dest)`**
    - **`zip_path`**: The path of the ZIP file.
    - **`dest`**: The destination directory to extract the files to.
    - **What it does**: Extracts files from the ZIP to the destination directory.

20. **`capture_photo(output_path)`**
    - **`output_path`**: The file path where the captured photo should be saved.
    - **What it does**: Captures a photo using the webcam and saves it to `output_path`.

21. **`record_video(output_path, duration)`**
    - **`output_path`**: The file path to save the recorded video.
    - **`duration`**: The duration in seconds for which to record the video.
    - **What it does**: Records a video using the webcam for the specified duration and saves it to `output_path`.

22. **`start_http_server(port)`**
    - **`port`**: The port on which the server should run.
    - **What it does**: Starts an HTTP server listening on the specified port.

23. **`get_server_status()`**
    - **What it does**: Checks and returns the current status of the HTTP server.

24. **`upload_file_to_server(file_path, url)`**
    - **`file_path`**: The path of the file to upload.
    - **`url`**: The server URL where the file should be uploaded.
    - **What it does**: Uploads a file to the server at the specified URL.

25. **`text_to_speech(text)`**
    - **`text`**: The text to convert into speech.
    - **What it does**: Converts the `text` into speech.

26. **`speech_to_text()`**
    - **What it does**: Records speech from the microphone and converts it into text.

27. **`get_cpu_usage()`**
    - **What it does**: Retrieves the current CPU usage percentage.

28. **`get_memory_usage()`**
    - **What it does**: Retrieves the current memory usage percentage.

29. **`get_ip_address()`**
    - **What it does**: Retrieves the system's current IP address.

30. **`safe_run(func)`**
    - **`func`**: The function to run safely.
    - **What it does**: Executes the function `func`, catching any exceptions and preventing the program from crashing.

31. **`track_mouse_position(callback)`**
    - **`callback`**: The function to call whenever the mouse position changes.
    - **What it does**: Tracks the mouse position and calls the `callback` when it moves.

32. **`run_shell_command(command)`**
    - **`command`**: The shell command to execute.
    - **What it does**: Runs a system shell command and returns the result.

33. **`send_email(subject, body, to_email)`**
    - **`subject`**: The subject of the email.
    - **`body`**: The body content of the email.
    - **`to_email`**: The recipient's email address.
    - **What it does**: Sends an email with the specified subject and body to the given recipient.

34. **`change_widget_bg_color(widget, color)`**
    - **`widget`**: The Tkinter widget.
    - **`color`**: The background color to apply to the widget.
    - **What it does**: Changes the background color of the widget.

35. **`change_widget_font(widget, font)`**
    - **`widget`**: The Tkinter widget.
    - **`font`**: The font to apply to the widget (e.g., `"Helvetica 12"`).
    - **What it does**: Changes the font of the widget.

36. **`add_widget_border(widget, width, color)`**
    - **`widget`**: The Tkinter widget.
    - **`width`**: The border width to apply.
    - **`color`**: The border color to apply.
    - **What it does**: Adds a border to the widget.

37. **`pack_with_padding(widget, padding)`**
    - **`widget`**: The Tkinter widget.
    - **`padding`**: The padding around the widget.
    - **What it does**: Packs the widget with the specified padding.

38. **`grid_widget(widget, row, column)`**
    - **`widget`**: The Tkinter widget.
    - **`row`**: The row in the grid where the widget should be placed.
    - **`column`**: The column in the grid where the widget should be placed.
    - **What it does**: Places the widget in a specific row and column in the grid.

39. **`place_widget(widget, x, y)`**
    - **`widget`**: The Tkinter widget.
    - **`x`**: The x-coordinate where to place the widget.
    - **`y`**: The y-coordinate where to place the widget.
    - **What it does**: Places the widget at the specified x and y coordinates.

40. **`delayed_pop(message, delay)`**
    - **`message`**: The message to display.
    - **`delay`**: The number of seconds to wait before displaying the message.
    - **What it does**: Displays a delayed pop-up message after the specified delay.

41. **`start_timer(duration, callback)`**
    - **`duration`**: The duration in seconds for the timer.
    - **`callback`**: The function to call when the timer finishes.
    - **What it does**: Starts a timer and triggers the `callback` after the specified duration.

42. **`get_weather(city, api_key)`**
    - **`city`**: The name of the city for which to get the weather.
    - **`api_key`**: The API key for accessing the weather API.
    - **What it does**: Retrieves the weather data for the specified city using an external weather API.

43. **`copy_to_clipboard(text)`**
    - **`text`**: The text to copy to the clipboard.
    - **What it does**: Copies the given `text` to the clipboard.

44. **`paste_from_clipboard()`**
    - **What it does**: Pastes the text from the clipboard.

45. **`text_to_speech(text)`**
   - **`text`**: The text to be converted to speech.
   - **What it does**: Converts the given `text` into speech using the `pyttsx3` engine.

46. **`speech_to_text()`**
   - **What it does**: Records audio from the microphone and converts the spoken words to text using Google's speech recognition API.

47. **`start_timer(seconds, callback)`**
   - **`seconds`**: The number of seconds to run the timer for.
   - **`callback`**: The function to call once every second during the timer's countdown.
   - **What it does**: Runs a countdown timer for `seconds`, calling `callback()` once every second.

48. **`generate_random_string(length=15)`**
   - **`length`**: The desired length of the generated string.
   - **What it does**: Generates a random alphanumeric string of length `length`, with possible special characters.

49. **`find_files_by_extension(directory, extension)`**
   - **`directory`**: The directory to search in.
   - **`extension`**: The file extension to search for (e.g., `'.txt'`).
   - **What it does**: Returns a list of files in `directory` that have the given `extension`.

50. **`get_ip_address()`**
   - **What it does**: Returns the local IP address of the machine.

51. **`send_email(subject, body, to_email, mailname, mailpass)`**
   - **`subject`**: The subject of the email.
   - **`body`**: The body content of the email.
   - **`to_email`**: The recipient's email address.
   - **`mailname`**: The sender's email username.
   - **`mailpass`**: The sender's email password.
   - **What it does**: Sends an email using Gmail's SMTP server.

52. **`convert_image_to_grayscale(image_path, output_path)`**
   - **`image_path`**: The path to the image to convert.
   - **`output_path`**: The path to save the grayscale image.
   - **What it does**: Converts the given image to grayscale and saves it at `output_path`.

53. **`play_audio(text)`**
   - **`text`**: The text to be converted to speech.
   - **What it does**: Converts the given `text` to speech using `pyttsx3`.

54. **`record_audio()`**
    - **What it does**: Records audio from the microphone and converts it to text using speech recognition.

55. **`get_cpu_usage()`**
    - **What it does**: Returns the current CPU usage as a percentage.

56. **`get_memory_usage()`**
    - **What it does**: Returns the current memory usage as a percentage.

57. **`open_url(url)`**
    - **`url`**: The URL to open.
    - **What it does**: Opens the specified URL in the default web browser.

58. **`create_zip_file(source_dir, output_zip)`**
    - **`source_dir`**: The directory containing files to zip.
    - **`output_zip`**: The output path for the zip file.
    - **What it does**: Creates a ZIP file from the contents of the `source_dir`.

59. **`extract_zip_file(zip_file, extract_dir)`**
    - **`zip_file`**: The path to the zip file.
    - **`extract_dir`**: The directory to extract files into.
    - **What it does**: Extracts the contents of the ZIP file to `extract_dir`.

60. **`capture_screenshot(output_path)`**
    - **`output_path`**: The path to save the screenshot.
    - **What it does**: Takes a screenshot of the current screen and saves it to `output_path`.

61. **`move_file(source, destination)`**
    - **`source`**: The file path of the source file.
    - **`destination`**: The file path to move the file to.
    - **What it does**: Moves a file from `source` to `destination`.

62. **`copy_file(source, destination)`**
    - **`source`**: The file path of the source file.
    - **`destination`**: The file path to copy the file to.
    - **What it does**: Copies a file from `source` to `destination`.

63. **`show_file_properties(file_path)`**
    - **`file_path`**: The path to the file.
    - **What it does**: Returns the file's size and last modified time.

63. **`check_website_status(url)`**
    - **`url`**: The URL of the website to check.
    - **What it does**: Returns `True` if the website is accessible (status code 200), else `False`.

65. **`run_shell_command(command)`**
    - **`command`**: The shell command to execute.
    - **What it does**: Executes a shell command and returns the output and any errors.

66. **`get_weather(city, api_key)`**
    - **`city`**: The name of the city to check the weather for.
    - **`api_key`**: The API key for accessing the weather service.
    - **What it does**: Retrieves the current weather for the specified city using the OpenWeatherMap API.

67. **`monitor_file_changes(file_path, callback)`**
    - **`file_path`**: The path to the file to monitor.
    - **`callback`**: The function to call when the file is modified.
    - **What it does**: Monitors the file for changes and calls `callback()` when the file is modified.

68. **`reverse_string(string)`**
    - **`string`**: The string to reverse.
    - **What it does**: Returns the reversed version of the input `string`.

69. **`calculate_factorial(number)`**
    - **`number`**: The number to calculate the factorial of.
    - **What it does**: Returns the factorial of `number`.

70. **`swap_values(a, b)`**
    - **`a`**: The first value.
    - **`b`**: The second value.
    - **What it does**: Returns `b` and `a` swapped.

71. **`find_maximum(numbers)`**
    - **`numbers`**: A list of numbers.
    - **What it does**: Returns the maximum value in the list `numbers`.

72. **`find_minimum(numbers)`**
    - **`numbers`**: A list of numbers.
    - **What it does**: Returns the minimum value in the list `numbers`.

73. **`get_random_choice(choices)`**
    - **`choices`**: A list of choices.
    - **What it does**: Returns a random element from the list `choices`.

74. **`generate_unique_id()`**
    - **What it does**: Generates and returns a unique ID using `uuid`.

75. **`concatenate_lists(list1, list2)`**
    - **`list1`**: The first list.
    - **`list2`**: The second list.
    - **What it does**: Returns a new list that is the concatenation of `list1` and `list2`.

76. **`write_to_file(filename, content)`**
    - **`filename`**: The file to write to.
    - **`content`**: The content to write to the file.
    - **What it does**: Writes `content` to the specified file.

77. **`read_from_file(filename)`**
    - **`filename`**: The file to read from.
    - **What it does**: Reads and returns the content of the specified file.

78. **`parse_json(json_string)`**
    - **`json_string`**: The JSON string to parse.
    - **What it does**: Parses the JSON string and returns the corresponding Python object.

79. **`create_file_if_not_exists(filename)`**
    - **`filename`**: The file to create if it doesn't exist.
    - **What it does**: Creates an empty file at `filename` if it doesn't already exist.

80. **`create_directory(directory)`**
    - **`directory`**: The directory to create if it doesn't exist.
    - **What it does**: Creates the specified directory if it doesn't already exist.

81. **`send_http_request(url, method='GET', data=None)`**
    - **`url`**: The URL to send the request to.
    - **`method`**: The HTTP method to use ('GET' or 'POST').
    - **`data`**: The data to send (only used with 'POST').
    - **What it does**: Sends an HTTP request to the specified `url` using the specified `method` and `data`, returning the response.

82. **`get_cpu_temperaturelinux()`**
    - **What it does**: Returns the CPU temperature (in Celsius) for Linux systems, or `None` if not available.

83. **`calculate_square_root(number)`**
    - **`number`**: The number to calculate the square root of.
    - **What it does**: Returns the square root of `number`.

84. **`track_mouse_position(callback)`**
    - **`callback`**: The function to call with the mouse's position as arguments.
    - **What it does**: Tracks the mouse position and calls `callback()` with the current `(x, y)` position.
85. **`show_error_messagebox(message)`**  
   - **`message`**: The error message to display.  
   - **What it does**: Displays a message box with the title "Error" and the provided message.
86. **`start_background_task(backtask)`**  
   - **`backtask`**: The function to execute in the background.  
   - **What it does**: Starts a separate thread to run the provided function without blocking the main program.

87. **`nocrash(func)`**  
   - **`func`**: The function to wrap in a crash-preventing decorator.  
   - **What it does**: Executes the function safely, preventing unhandled exceptions from crashing the program.

88. **`contains_swears_better(text)`**  
   - **`text`**: The input string to check.  
   - **What it does**: Returns `True` if the text contains any profane words; otherwise, `False`.

89. **`filter_profanity_in_text(text)`**  
   - **`text`**: The input string to filter.  
   - **What it does**: Censors profanity in the provided text by replacing inappropriate words with asterisks.

90. **`speech_to_text_with_filter()`**  
   - **No arguments.**  
   - **What it does**: Listens for speech input, converts it to text, and filters any profanity.

91. **`get_system_uptime()`**  
   - **No arguments.**  
   - **What it does**: Returns the system uptime in seconds since the last boot.

92. **`download_image_from_url(image_url, save_path)`**  
   - **`image_url`**: The URL of the image to download.  
   - **`save_path`**: The local path to save the image.  
   - **What it does**: Downloads an image from the specified URL and saves it to the given path.

93. **`monitor_new_files(directory, callback)`**  
   - **`directory`**: The folder to monitor.  
   - **`callback`**: The function to call when new files are detected.  
   - **What it does**: Continuously checks the directory for new files and triggers the callback with the new file names.

94. **`check_if_file_exists(file_path)`**  
   - **`file_path`**: The path of the file to check.  
   - **What it does**: Returns `True` if the file exists, otherwise `False`.

95. **`check_internet_connection()`**  
   - **No arguments.**  
   - **What it does**: Pings a server (e.g., Google) to check for an active internet connection. Returns `True` if connected.

96. **`create_web_server(directory, port=8000)`**  
   - **`directory`**: The directory to serve files from.  
   - **`port`**: The port number for the web server (default: 8000).  
   - **What it does**: Starts a simple HTTP server that serves files from the specified directory.

97. **`create_web_server(html, port=8000)`**  
   - **`html`**: The HTML content to serve.  
   - **`port`**: The port number for the web server (default: 8000).  
   - **What it does**: Hosts a web server displaying the provided HTML content.

98. **`uppercase_list(lst)`**  
   - **`lst`**: A list of strings.  
   - **What it does**: Converts each string in the list to uppercase and returns the modified list.

99. **`remove_duplicates(lst)`**  
   - **`lst`**: A list of items.  
   - **What it does**: Removes duplicate elements from the list and returns a new list with unique items.

100. **`find_index(lst, element)`**  
   - **`lst`**: The list to search.  
   - **`element`**: The element to find.  
   - **What it does**: Returns the index of the element in the list, or `-1` if not found.

101. **`random_element(lst)`**  
   - **`lst`**: A list of items.  
   - **What it does**: Returns a random item from the list, or `None` if the list is empty.

102. **`validate_email(email)`**  
   - **`email`**: The email address to validate.  
   - **What it does**: Returns `True` if the email matches a standard pattern; otherwise, `False`.

103. **`split_into_chunks(text, chunk_size)`**  
   - **`text`**: The string to split.  
   - **`chunk_size`**: The size of each chunk.  
   - **What it does**: Splits the text into smaller chunks of the specified size and returns a list of chunks.  

104. `evaluate_text_length(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Splits the input text into sentences and words. Calculates the average length of words and the average number of words per sentence. Returns a tuple containing the average word length and the average sentence length.  

105. `sentiment_analysis(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Analyzes the sentiment of the text and returns:
     - "Positive" if the sentiment is positive.
     - "Negative" if the sentiment is negative.
     - "Non Pos Non Neg" if the sentiment is neutral.

106. `analyze_text(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Performs a comprehensive analysis of the text, including:
     - Word count, sentence count, word frequencies, sentiment analysis, average word and sentence length, and keyword extraction.  
   - **Returns**: A dictionary containing all analysis results.

107. `unique_elements(lst)`**  
   - **`lst`**: The list of elements.  
   - **What it does**: Removes duplicate elements from the list and returns a list of unique elements.

108. `sum_list(lst)`**  
   - **`lst`**: The list of numbers.  
   - **What it does**: Sums all the numbers in the list and returns the total sum.

109. `reverse_list(lst)`**  
   - **`lst`**: The list of elements.  
   - **What it does**: Reverses the order of elements in the list and returns the reversed list.

110. `is_prime(n)`**  
   - **`n`**: The number to check for primality.  
   - **What it does**: Checks if the number `n` is prime by testing divisibility from 2 up to the square root of `n`. Returns `True` if the number is prime, and `False` otherwise.

111. `shorten_text(text, length)`**  
   - **`text`**: The string to shorten.  
   - **`length`**: The maximum length of the shortened string.  
   - **What it does**: Shortens the input text to the specified length. If the text is longer than the length, it appends "..." at the end.

112. `word_count(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Counts the number of words in the text and returns the word count.

113. `is_valid_phone_number(phone_number)`**  
   - **`phone_number`**: The phone number to validate.  
   - **What it does**: Validates the phone number based on a regular expression pattern. Returns `True` if the phone number matches the pattern (international format), otherwise returns `False`.

114. `clean_null(data)`**  
   - **`data`**: The list or dictionary to clean.  
   - **What it does**: Removes `None`, empty strings, empty lists, empty dictionaries, and `False` values from the data. Returns the cleaned list or dictionary.

115. `calculate_average(numbers)`**  
   - **`numbers`**: The list of numbers to average.  
   - **What it does**: Calculates the average (mean) of the numbers in the list. Returns the average value. If the list is empty, returns `0`.

116. `calculate_median(numbers)`**  
   - **`numbers`**: The list of numbers to find the median.  
   - **What it does**: Sorts the numbers and calculates the median:
     - If the list has an odd number of elements, returns the middle number.
     - If the list has an even number of elements, returns the average of the two middle numbers.

117. `count_words(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Counts the number of words in the text by identifying word boundaries and returns the word count.

118. `count_sentences(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Counts the number of sentences in the text by splitting it based on sentence-ending punctuation (e.g., `.`, `!`, `?`). Returns the sentence count.

119. `word_frequencies(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Calculates the frequency of each word in the text (case-insensitive) and returns a dictionary with words as keys and their frequencies as values.

120. `common_words(text1, text2)`**  
   - **`text1`**: The first string to compare.  
   - **`text2`**: The second string to compare.  
   - **What it does**: Finds the common words between the two input texts. Returns a list of the words that appear in both texts.

121. `extract_keywords(text, n=5)`**  
   - **`text`**: The string to analyze.  
   - **`n`**: The number of keywords to extract (default is 5).  
   - **What it does**: Extracts the top `n` keywords from the text using the **TF-IDF** (Term Frequency-Inverse Document Frequency) method, excluding common stop words. Returns a list of the top `n` keywords based on their importance.

 122. **`evaluate_text_length(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Analyzes the text and calculates two key metrics:  
     - **Average word length**: The average number of characters per word.  
     - **Average sentence length**: The average number of words per sentence.  
   - **Returns**: A tuple containing `avg_word_length` and `avg_sentence_length`.

 123. **`sentiment_analysis(text)`**  
   - **`text`**: The string to analyze.  
   - **What it does**: Performs sentiment analysis using **TextBlob** to determine whether the text is:
     - Positive (if the polarity score is greater than 0),
     - Negative (if the polarity score is less than 0),
     - Neutral (if the polarity score is exactly 0).  
   - **Returns**: A string: `"Positive"`, `"Negative"`, or `"Non Pos Non Neg"`.

 124. **`Jai(question)`**  
   - **`question`**: A string containing the question you want to ask.  
   - **What it does**: Uses **JynAi** to get an answer.**Use internet for better answers!**
   - **Returns**: A string containing the generated response.

 125. **`replace(string, replacement, replacment)`**  
   - **`string`**: The original string.  
   - **`replacement`**: The substring to be replaced.  
   - **`replacment`**: The new substring that will replace the old one.  
   - **What it does**: Replaces the first substring (`replacement`) in the original string with the new substring (`replacment`).  
   - **Returns**: The modified string with the replacement.

 126. **`containsstr(string1, wic)`**  
   - **`string1`**: The string to search within.  
   - **`wic`**: The characters or substring to look for.  
   - **What it does**: Checks if the string contains any of the characters or substrings provided in `wic`. It uses regular expressions to search for the matches.  
   - **Returns**: `True` if any matching characters or substrings are found; otherwise, `False`.

 127. **`split(string, strip_chars)`**  
   - **`string`**: The string to split.  
   - **`strip_chars`**: Characters to remove from the string.  
   - **What it does**: Removes the specified characters (`strip_chars`) from the string and returns the cleaned string.  
   - **Returns**: The string with the specified characters removed.

 128. **`contamath_beta(func)`**  
   - **`func`**: The string or expression to check.  
   - **What it does**: Checks if the provided string or expression (`func`) contains any mathematical operators (`+`, `-`, `*`, `/` and more).  
   - **Returns**: `True` if any mathematical operator is present; otherwise, `False`.

 129. **`show_window(root)`**
   - **What it does**: Shows the windows based on root name. 

 130. **`add_commas(input_string)`**  
   - **`input_string`**: The string you want to add commas to.  
   - **What it does**: Joins each character of the input string with a comma between them.  
   - **Returns**: A string with commas inserted between each character of the input string.  
   
 131. **`remove_spaces(text)`**  
   - **`text`**: The string from which you want to remove spaces.  
   - **What it does**: Removes all spaces from the given string.  
   - **Returns**: A string without spaces.

 132. **`remove_spaces_andstickT(text)`**  
   - **`text`**: The string from which spaces are to be removed.  
   - **What it does**: Uses a regular expression to remove all types of whitespace characters from the input text.  
   - **Returns**: A string with all spaces removed.  

 133. **`delfs(input_string, text_to_delete)`**  
   - **`input_string`**: The string from which a specified text will be removed.  
   - **`text_to_delete`**: The substring that will be deleted from the input string.  
   - **What it does**: Removes all instances of `text_to_delete` from the input string.  
   - **Returns**: A string with the specified text removed.

 134. **`rem_alphabet(text)`**  
   - **`text`**: The string from which alphabetic characters will be removed.  
   - **What it does**: Filters out all alphabetic characters (both uppercase and lowercase) from the string.  
   - **Returns**: A string containing only non-alphabetic characters.

 135. **`contamath_beta(func)`**  
   - **`func`**: The string or expression to check.  
   - **What it does**: Checks if the provided string or expression (`func`) contains any mathematical operators (`+`, `-`, `*`, `/`, or others).  
   - **Returns**: `True` if any mathematical operator is present; otherwise, `False`.

 136. **`add_commas(input_string)`**
   - **`input_string`**: The string to which commas need to be added.
   - **What it does**: Takes an input string and inserts commas between each character.
   - **Returns**: A string with commas between each character.

 137. **`remove_spaces(text)`**
   - **`text`**: The string from which spaces need to be removed.
   - **What it does**: Removes all spaces from the provided string.
   - **Returns**: A new string with no spaces.

 138. **`remove_spaces_andstickT(text)`**
   - **`text`**: The string from which spaces need to be removed.
   - **What it does**: Uses a regular expression to remove all whitespace (including tabs, newlines, etc.) from the string.
   - **Returns**: A new string without any spaces or whitespace characters.

 139. **`delfs(input_string, text_to_delete)`**
   - **`input_string`**: The string from which the text needs to be deleted.
   - **`text_to_delete`**: The substring that should be removed from the input string.
   - **What it does**: Removes the specified `text_to_delete` from the `input_string`.
   - **Returns**: A new string with the specified text deleted.

 140. **`rem_alphabet(text)`**
   - **`text`**: The string from which alphabetic characters need to be removed.
   - **What it does**: Removes all alphabetic characters (letters) from the provided string, keeping only numbers and symbols.
   - **Returns**: A new string with no alphabetic characters.

 141. **`hotdog(k1="", k2="", k3="", k4="", k5="")`**
   - **`k1, k2, k3, k4, k5`**: The keys to be pressed.
   - **What it does**: Simulates pressing a sequence of keys using `pyautogui`’s `hotkey` function. The arguments correspond to keyboard keys.
   - **Returns**: No return value (action is executed on the system).

 142. **`keypress(key)`**
   - **`key`**: The key to simulate pressing.
   - **What it does**: Simulates pressing a single key on the keyboard using `pyautogui`.
   - **Returns**: No return value (action is executed on the system).

 143. **`isequal(s, eq)`**
   - **`s`**: The string to compare.
   - **`eq`**: The string to check against.
   - **What it does**: Compares two strings, ignoring case, and checks if they are equal.
   - **Returns**: `True` if both strings are equal (case-insensitive), otherwise `False`.

 144. **`contains(s, eq)`**
   - **`s`**: The string to check.
   - **`eq`**: The substring to search for.
   - **What it does**: Checks if the string `s` contains the substring `eq`, ignoring case.
   - **Returns**: `True` if the substring `eq` is found within `s`, otherwise `False`.

 145. **`LoadingBar` (Class)**
   - **Attributes**: 
     - `total_steps`: The total number of steps to represent in the loading bar.
     - `bar_length`: The length of the loading bar (default is 40).
     - `progress`: The current progress in the loading process.
   - **Methods**:
     - **`load()`**: Updates the loading bar and displays the current progress.
     - **`finish()`**: Marks the completion of the loading process by displaying a 100% progress bar.

 146. **`track_function_start_end(func)`**
   - **`func`**: The function to track the execution of.
   - **What it does**: Wraps a function to track its execution and update the loading bar each time the function starts or finishes.
   - **Returns**: The original function result.

 147. **`loading_bar(code)`**
   - **`code`**: A string containing Python code to execute.
   - **What it does**: Counts the number of function calls in the provided code and creates a loading bar to track the execution of each function. The code is executed while the loading bar is updated in real-time.
   - **Returns**: No return value; the code is executed and the loading bar is displayed.

 148. `nolim(func)`**
   - **`func`**: A function that you want to apply the decorator to.
   - **What it does**: This is a decorator that modifies the maximum number of digits allowed when converting an integer to a string. It sets the system's integer digit limit (`sys.set_int_max_str_digits`) to `99 * 99 * 99` (970299), preventing excessive number lengths during string conversion operations.
   - **Returns**: The original function `func` after modifying the system's digit limit. The function is executed as normal, but with the updated integer-to-string digit limit in place.

 149. `parallel(*functions)`
   - **`*functions`**: A list of functions to run in parallel.
   - **What it does**: This function executes the provided functions concurrently by creating a new thread for each function. It starts each thread simultaneously, and waits for all threads to finish using `thread.join()`.
   - **Returns**: No return value; the functions are executed concurrently, and the program waits for all of them to complete before moving forward.

 150. `gs(func)`
   - **`func`**: A function whose source code you want to retrieve.
   - **What it does**: This function uses Python's `inspect.getsource()` method to retrieve and return the source code of the provided function `func` as a string.
   - **Returns**: A string containing the source code of the function `func`.

 151. `ccc(core_count, function, *args, **kwargs)`
   - **`core_count`**: The number of CPU cores you want the function to run on.
   - **`function`**: The function to execute.
   - **`*args, **kwargs`**: Additional arguments and keyword arguments passed to the function.
   - **What it does**: This function sets the CPU affinity to the specified number of cores (`core_count`) before executing the function. It ensures that the function is only executed on the specified number of cores. If `core_count` exceeds the available number of cores, it raises a `ValueError`.
   - **Returns**: The result of the executed function, with the specified CPU cores applied for the execution.

 152. `wait(key="s",num=1)`
   - **`key`**: The key value to pick `(s --> second ,m --> minute ,h --> hour)`.
   - **`num`**: The number of `s/m/h` to wait.
   - **What it does**: This function waits the same thing that is with time.sleep function but advantaged
   - **Returns**: Nothing just waits as like `time.sleep`.

 153. `Jynauth(func, user_name, app_name)`
   - **`func`**: The function to execute after successful authentication. This function is passed as an argument and will be called once the OTP is verified correctly.
   - **`user_name`**: The user's name, which is used in the QR code URI as part of the `issuer` field.
   - **`app_name`**: The name of the app, which is included in the QR code URI to link the user with the specific application.
   - **What it does**: 
     - This function manages the entire process of setting up Two-Factor Authentication (2FA) using Time-based One-Time Passwords (TOTP).
     - It generates a secret key, creates a QR code that can be scanned by an authenticator app, and provides a user interface to verify the OTP input by the user.
     - Once the user inputs the OTP from their authenticator app, the provided function (`func`) is executed if the OTP is correct.
   - **Returns**: 
     - Nothing directly. It creates a window with the QR code and waits for the user to verify the OTP.

 154. `Jwin`
   The `Jwin` class creates a Tkinter window where widgets are dynamically configured and displayed based on the layout and configuration provided. The widgets supported are created and managed in a grid layout. Here's how each widget works inside `Jwin`:

1. **Button Widget**  
   - **Widget Type**: `"button"`
   - **Configuration**: In `widgets_config`, you can define a button with the widget type as `"button"`. You also define the `position` (which row and column it should be placed in) and optional configuration such as the `"text"` (button label) and `"id"` (a unique identifier for callbacks).
   - **Behavior**: When the button is clicked, the corresponding callback function (if defined in `user_callbacks`) is executed.
   - **Example**:
     ```python
     {"type": "button", "position": (0, 0), "options": {"text": "Click Me", "id": "button1"}}
     ```

2. **Label Widget**  
   - **Widget Type**: `"label"`
   - **Configuration**: A label widget displays text. You specify the `position` and optionally set the `"text"` and `"id"` for identification.
   - **Behavior**: This widget is for displaying static text in the window.
   - **Example**:
     ```python
     {"type": "label", "position": (1, 0), "options": {"text": "This is a label", "id": "label1"}}
     ```

3. **Input Field Widget**  
   - **Widget Type**: `"input"`
   - **Configuration**: An input field where users can type text. You can define its position and optionally provide an `"id"`.
   - **Behavior**: Users can enter text, and the value can be retrieved using the `get_value` method.
   - **Example**:
     ```python
     {"type": "input", "position": (2, 0), "options": {"id": "input1"}}
     ```

4. **Password Field Widget**  
   - **Widget Type**: `"password"`
   - **Configuration**: A password input field that hides the entered text (replaces with asterisks). Like the regular input field, it can be configured with `position` and `"id"`.
   - **Behavior**: This widget hides user input and allows for secure text entry.
   - **Example**:
     ```python
     {"type": "password", "position": (3, 0), "options": {"id": "password1"}}
     ```

5. **Checkbox Widget**  
   - **Widget Type**: `"checkbox"`
   - **Configuration**: A checkbox allows the user to toggle a true/false value. The `position` and `"text"` can be customized, and it can also have an `"id"`.
   - **Behavior**: Users can toggle the checkbox on or off, and the state can be retrieved using `get_value`.
   - **Example**:
     ```python
     {"type": "checkbox", "position": (0, 1), "options": {"text": "Accept Terms", "id": "checkbox1"}}
     ```

6. **Dropdown (Combobox) Widget**  
   - **Widget Type**: `"dropdown"`
   - **Configuration**: A dropdown menu that allows the user to select one option from a list. You define the `position`, a list of `"values"` to populate the dropdown, and optionally an `"id"`.
   - **Behavior**: Users can select an option from the dropdown, and the selected value can be retrieved using `get_value`.
   - **Example**:
     ```python
     {"type": "dropdown", "position": (1, 1), "options": {"values": ["Option 1", "Option 2"], "id": "dropdown1"}}
     ```

7. **Radio Buttons Widget**  
   - **Widget Type**: `"radio"`
   - **Configuration**: A group of radio buttons where users can choose one option. The `position` and `values` for each button can be set. Each radio button will share the same `"id"`.
   - **Behavior**: Users can select one of the options, and the selected value is saved in a variable. You can retrieve the selected value using `get_value`.
   - **Example**:
     ```python
     {"type": "radio", "position": (2, 1), "options": {"values": ["Option A", "Option B"], "id": "radio1"}}
     ```

8. **Textarea Widget**  
   - **Widget Type**: `"textarea"`
   - **Configuration**: A multi-line text area where users can input large amounts of text. You specify the `position` and an optional `"id"`.
   - **Behavior**: The user can enter multiple lines of text, which can be retrieved using `get_value`.
   - **Example**:
     ```python
     {"type": "textarea", "position": (3, 1), "options": {"id": "textarea1"}}
     ```

9. **Slider Widget**  
   - **Widget Type**: `"slider"`
   - **Configuration**: A slider widget that lets users select a value within a specified range. You define `position`, `min` and `max` values, and optionally an `"id"`.
   - **Behavior**: Users can slide the slider to select a value, which can be retrieved using `get_value`.
   - **Example**:
     ```python
     {"type": "slider", "position": (0, 2), "options": {"min": 0, "max": 100, "id": "slider1"}}
     ```

10. **Listbox Widget**  
    - **Widget Type**: `"listbox"`
    - **Configuration**: A listbox where multiple items can be displayed, and the user can select one. You define `position`, a list of `"values"`, and optionally an `"id"`.
    - **Behavior**: Users can select a single item from the list, which can be retrieved using `get_value`.
    - **Example**:
      ```python
      {"type": "listbox", "position": (1, 2), "options": {"values": ["Item 1", "Item 2", "Item 3"], "id": "listbox1"}}
      ```

11. **Canvas Widget**  
    - **Widget Type**: `"canvas"`
    - **Configuration**: A drawing area where you can add graphics. You specify the `position`, and optional `width` and `height` for the canvas.
    - **Behavior**: This widget allows you to draw graphics on it (e.g., lines, shapes, images). The canvas can be used for custom drawings and visualizations.
    - **Example**:
      ```python
      {"type": "canvas", "position": (2, 2), "options": {"width": 300, "height": 200, "id": "canvas1"}}
      ```

12. **Progressbar Widget**  
    - **Widget Type**: `"progressbar"`
    - **Configuration**: A progress bar that visually indicates progress. You can define the `position` and set the `mode` (e.g., "determinate" or "indeterminate").
    - **Behavior**: The progress bar can show the current progress or run in an indeterminate mode. You can control its value programmatically and retrieve its progress.
    - **Example**:
      ```python
      {"type": "progressbar", "position": (3, 2), "options": {"mode": "determinate", "id": "progressbar1"}}
      ```

13. **Spinbox Widget**  
    - **Widget Type**: `"spinbox"`
    - **Configuration**: A widget for selecting values within a defined range. You specify the `position`, `min`, `max`, and optionally an `"id"`.
    - **Behavior**: Users can select an integer value from the range by spinning up or down. The selected value can be retrieved using `get_value`.
    - **Example**:
      ```python
      {"type": "spinbox", "position": (0, 3), "options": {"min": 1, "max": 10, "id": "spinbox1"}}
      ```
 **For example**:

layout = """
+--------+--------+  
|12345678|12345678|  
|12345678|12345678|  
|12345678|12345678|  
+--------+--------+  
"""

# Define widgets with positions and options
widgets_config = [
    {"type": "spinbox", "position": (0, 3), "options": {"min": 1, "max": 10, "id": "spinbox1"}},
    {"type": "progressbar", "position": (3, 2), "options": {"mode": "determinate", "id": "progressbar1"}},
    {"type": "canvas", "position": (2, 2), "options": {"width": 300, "height": 200, "id": "canvas1"}},
    {"type": "listbox", "position": (1, 2), "options": {"values": ["Item 1", "Item 2", "Item 3"], "id": "listbox1"}},
    {"type": "slider", "position": (0, 2), "options": {"min": 0, "max": 100, "id": "slider1"}},
    {"type": "textarea", "position": (3, 1), "options": {"id": "textarea1"}},
    {"type": "radio", "position": (2, 1), "options": {"values": ["Option A", "Option B"], "id": "radio1"}},
    {"type": "dropdown", "position": (1, 1), "options": {"values": ["Option 1", "Option 2"], "id": "dropdown1"}},
    {"type": "checkbox", "position": (0, 1), "options": {"text": "Accept Terms", "id": "checkbox1"}},
    {"type": "password", "position": (3, 0), "options": {"id": "password1"}},
    {"type": "input", "position": (2, 0), "options": {"id": "input1"}},
    {"type": "label", "position": (1, 0), "options": {"text": "This is a label", "id": "label1"}},
    {"type": "button", "position": (0, 0), "options": {"text": "Click Me", "id": "button1"}},
]

# Default callbacks
def button_click_callback():
    print("Button clicked!")
    slider_callback()  # Example of chaining callbacks

def checkbox_callback():
    print("Checkbox state changed!")

def slider_callback():
    slider_value = Jwin.get_value("slider1")  # Retrieve slider value dynamically
    print("Slider value:", slider_value)

def spinbox_callback():
    spinbox_value = Jwin.get_value("spinbox1")  # Get value from spinbox widget
    print("Spinbox value:", spinbox_value)

def progressbar_callback():
    progress_value = Jwin.get_value("progressbar1")  # Get progress from progressbar widget
    print("Progress bar value:", progress_value)

def canvas_callback():
    print("Canvas interaction (e.g., drawing or click) occurred!")

def listbox_callback():
    selected_item = Jwin.get_value("listbox1")  # Get selected item from listbox
    print("Listbox selected item:", selected_item)

def textarea_callback():
    text_value = Jwin.get_value("textarea1")  # Get text from textarea widget
    print("TextArea content:", text_value)

def radio_callback():
    selected_option = Jwin.get_value("radio1")  # Get selected radio button option
    print("Radio button selected option:", selected_option)

def dropdown_callback():
    selected_option = Jwin.get_value("dropdown1")  # Get selected dropdown option
    print("Dropdown selected option:", selected_option)

def password_callback():
    password_value = Jwin.get_value("password1")  # Get entered password from password field
    print("Password entered:", password_value)

def input_callback():
    input_value = Jwin.get_value("input1")  # Get input field value
    print("Input field value:", input_value)

def label_callback():
    print("Label was interacted with!")

# User-defined callback functions for each widget
user_callbacks = {
    "button1": button_click_callback,        # Button callback
    "checkbox1": checkbox_callback,          # Checkbox callback
    "slider1": slider_callback,              # Slider callback
    "spinbox1": spinbox_callback,            # Spinbox callback
    "progressbar1": progressbar_callback,    # Progress bar callback
    "canvas1": canvas_callback,              # Canvas callback
    "listbox1": listbox_callback,            # Listbox callback
    "textarea1": textarea_callback,          # Textarea callback
    "radio1": radio_callback,                # Radio button callback
    "dropdown1": dropdown_callback,          # Dropdown callback
    "password1": password_callback,          # Password callback
    "input1": input_callback,                # Input callback
    "label1": label_callback,                # Label callback
}

  155. ``exists(Filename")``:
    The `Filename` is checks if the file exists.

  156. ``Jctb("input string")  /  Jbtc("input string")``
    **Jctb:**` input string` is input itll return a binary code that can only be undoed by the `Jbtc` function.
    **Jbtc:**` input string` is input thatll only accept the binary code that maden with `Jctb` function and return the actual string.

  157. ``get_curr_dir()``:
    Returns the current directory the program is runnig.