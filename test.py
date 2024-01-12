import json
import re
import string

myString = """```json
{
  "table": {
    "caption": "Debt securities",
    "headers": [
      {
        "value": "As of",
        "colspan": 3
      },
      {
        "value": "December 31, 2022",
        "colspan": 3
      }
    ],
    "rows": [
      [
        {
          "value": "Due in 1 year or less"
        },
        {
          "value": 16083
        }
      ],
      [
        {
          "value": "Due in 1 year through 5 years"
        },
        {
          "value": 11370
        }
      ],
      [
        {
          "value": "Due in 5 years through 10 years"
        },
        {
          "value": 8170
        }
      ],
      [
        {
          "value": "Due after 10 years"
        },
        {
          "value": 11580
        }
      ],
      [
        {
          "value": "Total"
        },
        {
          "value": 87531
        }
      ]
    ]
  }
}
```

```json
{
  "table": {
    "caption": "As of December 31, 2022",
    "headers": [
      {
        "value": "Less than 12 Months or Greater",
        "colspan": 3
      },
      {
        "value": "12 Months or Greater",
        "colspan": 3
      },
      {
        "value": "Total",
        "colspan": 3
      }
    ],
    "rows": [
      [
        {
          "value": "Corporate debt securities"
        },
        {
          "value": 22378
        },
        {
          "value": (236)
        },
        {
          "value": 71
        },
        {
          "value": (2)
        },
        {
          "value": 22449
        },
        {
          "value": (238)
        }
      ],
      [
        {
          "value": "Government bonds"
        },
        {
          "value": 6737
        },
        {
          "value": (106)
        },
        {
          "value": 303
        },
        {
          "value": (6)
        },
        {
          "value": 7040
        },
        {
          "value": (112)
        }
      ],
      [
        {
          "value": "Mortgage-backed and asset-backed securities"
        },
        {
          "value": 11502
        },
        {
          "value": (494)
        },
        {
          "value": 622
        },
        {
          "value": (3)
        },
        {
          "value": 11750
        },
        {
          "value": (507)
        }
      ],
      [
        {
          "value": "Total"
        },
        {
          "value": 37617
        },
        {
          "value": (836)
        },
        {
          "value": 996
        },
        {
          "value": (11)
        },
        {
          "value": 38613
        },
        {
          "value": (857)
        }
      ]
    ]
  }
}
```

```json
{
  "table": {
    "caption": "As of December 31, 2021",
    "headers": [
      {
        "value": "Less than 12 Months or Greater",
        "colspan": 3
      },
      {
        "value": "12 Months or Greater",
        "colspan": 3
      },
      {
        "value": "Total",
        "colspan": 3
      }
    ],
    "rows": [
      [
        {
          "value": "Corporate debt securities"
        },
        {
          "value": 21039
        },
        {
          "value": (1004)
        },
        {
          "value": 13438
        },
        {
          "value": (1041)
        },
        {
          "value": 34477
        },
        {
          "value": (2045)
        }
      ],
      [
        {
          "value": "Government bonds"
        },
        {
          "value": 7225
        },
        {
          "value": (440)
        },
        {
          "value": 6964
        },
        {
          "value": (657)
        },
        {
          "value": 14189
        },
        {
          "value": (1097)
        }
      ],
      [
        {
          "value": "Mortgage-backed and asset-backed securities"
        },
        {
          "value": 11228
        },
        {
          "value": (855)
        },
        {
          "value": 15125
        },
        {
          "value": (1052)
        },
        {
          "value": 26353
        },
        {
          "value": (1907)
        }
      ],
      [
        {
          "value": "Total"
        },
        {
          "value": 39492
        },
        {
          "value": (2309)
        },
        {
          "value": 35527
        },
        {
          "value": (2750)
        },
        {
          "value": 75019
        },
        {
          "value": (4759)
        }
      ]
    ]
  }
}
```

```json
{
  "table": {
    "caption": "Year Ended December 31,",
    "headers": [
      {
        "value": "2022",
        "colspan": 2
      },
      {
        "value": "2021",
        "colspan": 2
      }
    ],
    "rows": [
      [
        {
          "value": "Unrealized gain (loss) on fair value option debt securities"
        },
        {
          "value": 86
        },
        {
          "value": (122)
        }
      ],
      [
        {
          "value": "Gross realized gain on debt securities"
        },
        {
          "value": 899
        },
        {
          "value": 432
        }
      ],
      [
        {
          "value": "Gross realized loss on debt securities"
        },
        {
          "value": (184)
        },
        {
          "value": (329)
        }
      ],
      [
        {
          "value": "(Increase) decrease in allowance for credit losses"
        },
        {
          "value": 76
        },
        {
          "value": 91
        }
      ],
      [
        {
          "value": "Total"
        },
        {
          "value": 725
        },
        {
          "value": (264)
        }
      ]
    ]
  }
}
``` """

def convert_string_to_json(string):
    """Converts a string to a JSON object.

    Args:
        string: The string to convert to a JSON object.

    Returns:
        A JSON object.
    """

    json_object = json.loads(string)
    return json_object

def replace_numbers_between_parentheses(string):
  """Replaces numbers between parentheses with the same number with a negative sign.

  Args:
    string: The string to search.

  Returns:
    The string with the numbers between parentheses replaced.
  """

  # Find all numbers between parentheses.
  numbers = re.findall(r"\((\d+)\)", string)

  # Replace each number with the same number with a negative sign.
  for number in numbers:
    string = string.replace("({})".format(number), f"-{number}")

  return string


if __name__ == '__main__':
  

  prompt = ["""Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data, all the columns and rows faithfully represented as well as the headers. 
              Consistency of the format is key and the output format should always be as followed: every single table will have a JSON Document starting only with '```json' and end '```'""",
  """Extract every table from top to bottom as it appears in the image and generate one JSON document per table discovered with all the information about the date (month, year,...) for this data."""]
  
  test = False

  print(int(test))


  contents_restrictive = [
      prompt[0]
  ]

  contents_restrictive = [
      prompt[1]
  ]


# Read the JSON string from a file

    #print (myString)
    #search_expression ="{}(.+?)".format("json") 

    #print (myString.find("json"))
    #print (myString.replace("```", ""))

    # myString = myString.replace("```", "")
    # myString = replace_numbers_between_parentheses(myString)
    # answers = myString.split("json")

    # proper_list = [answer for answer in answers if len(answer) > 0]



    # for i, answer in enumerate(proper_list):
    #     myJsonObj = convert_string_to_json(answer)
        
    #     print(i)
    #     print(myJsonObj)


    #m = re.search(search_expression, myString)

    #m = re.search('json(.+?)json', myString)

    #print(m.group(1))