flowchart TD
    %% Nodes definition
    Start([Start])
    Login[/Login/]
    Signup[/Signup/]
    LoginCheck{"Login Successful?"}
    DisplayUI("(Display the UI of app)")
    
    Checklist[/"Checklist Box:\nItems to Pack?"/]
    SaveItem{"Save stored item?"}
    Forget("(Forget.)")
    SQLite("(SQLite stores the data)")
    
    HolidayInput[/"Input:\nHoliday Destination?"/]
    ValidInput{"Valid Input?"}
    WeatherAPI("(OpenWeatherMapAPI:\nGetting weather info)")
    NewsAPI("(NewsAPI:\nGet input news)")
    
    Finish([Finish])

    %% Flow connections
    Start --> Login
    Start --> Signup
    
    Signup --> Login
    Login --> LoginCheck
    
    LoginCheck -- No --> Login
    LoginCheck -- Yes --> DisplayUI
    
    %% Left Branch (Checklist)
    DisplayUI --> Checklist
    Checklist --> SaveItem
    SaveItem -- No --> Forget
    SaveItem -- Yes --> SQLite
    SQLite --> Finish
    
    %% Right Branch (Holiday Input)
    DisplayUI --> HolidayInput
    HolidayInput --> ValidInput
    ValidInput -- No --> HolidayInput
    ValidInput -- Yes --> WeatherAPI
    ValidInput -- Yes --> NewsAPI
    WeatherAPI --> Finish
