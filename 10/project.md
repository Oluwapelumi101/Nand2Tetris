Ranking
- Moba (Best pay / 3 years afterwards)
- PSW (Intresting Projects / Low pay)
- Konzept (Nice location & Intresting Projects / Lowest pay)
- Jetter (Highest pay in BW / farthest from Software)

Tokenizer
- Parser
- Output in Xml

Tokenizing
- Open Jack file
- Parse out comment 
- Parse out spaces
- Take each word and symbol in a line and convert to a token (parsing on Space, exception case "new/(), get()")
- Convert entire input to a stream of token
- Each token is encased by its type
    - <keyword>if</keywprd>
    - Token type in the case, token value in the middle

- Determine input type (string, int)
- Determin if input is a reserved word
- Use the follwing to determing the token classification
- Encase the token value in the class
- Store in output list
- Handling special characters
- String without double coats


Token Category
- Keyword
- Symbol
- Integer Const
- String Const
- Identifers