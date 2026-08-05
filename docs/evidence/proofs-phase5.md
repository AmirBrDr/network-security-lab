 amir@Amirmahdis-MacBook-Pro  ~  curl -s http://127.0.0.1:11434/api/chat \
>   -H "Content-Type: application/json" \
>   -d '{
>     "model": "qwen2.5-coder:7b-instruct",
>     "stream": false,
>     "messages": [
>       {
>         "role": "system",
>         "content": "You are a cautious network security lab assistant. Answer only from supplied evidence."
>       },
>       {
>         "role": "user",
>         "content": "Explain in one paragraph what an OSPF neighbor loss alert usually means."
>       }
>     ]
>   }' | jq
{
  "model": "qwen2.5-coder:7b-instruct",
  "created_at": "2026-08-05T18:09:12.269884Z",
  "message": {
    "role": "assistant",
    "content": "An OSPF (Open Shortest Path First) neighbor loss alert indicates that a device has lost contact with another OSPF-enabled device on the same network segment or area. This typically happens when there is a failure in communication between routers, which can be due to various reasons such as link failures, configuration errors, or network congestion. The alert prompts network administrators to investigate and resolve the issue to maintain proper routing and prevent potential network outages."
  },
  "done": true,
  "done_reason": "stop",
  "total_duration": 6859793875,
  "load_duration": 3202857000,
  "prompt_eval_count": 43,
  "prompt_eval_duration": 592024375,
  "eval_count": 89,
  "eval_duration": 3022455751
}
 amir@Amirmahdis-MacBook-Pro  ~  




 amir@Amirmahdis-MacBook-Pro  ~  curl -s http://127.0.0.1:11434/api/generate \
>   -H "Content-Type: application/json" \
>   -d '{
>     "model": "llama3.2:3b",
>     "stream": false,
>     "prompt": "Summarize this event: R2 has fewer than two Full OSPFv2 neighbors."
>   }' | jq
{
  "model": "llama3.2:3b",
  "created_at": "2026-08-05T18:14:47.729283Z",
  "response": "When an R2 (Routing Layer 2) device reports \"fewer than two Full OSPFv2 neighbors\", it means that the router is unable to establish or maintain a full adjacency with at least two other OSPFv2 neighbors.\n\nOSPFv2 (Open Shortest Path First version 2) is a routing protocol used for inter-autonomous system communications. A Full OSPFv2 neighbor is required for the router to achieve optimal routing and network topology discovery.\n\nIn this scenario, R2 may be experiencing one of the following issues:\n\n1. **Neighbor adjacency failure**: The router may not have been able to establish an adjacency with at least two neighbors due to configuration errors, lack of connectivity, or other networking issues.\n2. **Lack of OSPFv2 protocol enablement**: One or more neighboring routers might not be configured to run OSPFv2, causing the R2 device to not have a full set of neighbors.\n3. **Network topology limitations**: The network topology might be such that it's difficult for the router to establish multiple full OSPFv2 adjacencies.\n\nTo resolve this issue, you would typically need to:\n\n1. Verify and correct any configuration errors.\n2. Check network connectivity and ensure that all neighboring routers are reachable.\n3. Adjust the OSPFv2 protocol settings on one or more neighboring routers if necessary.\n4. Investigate and address any underlying network topology issues.\n\nIf left unaddressed, this issue may result in suboptimal routing performance and potential connectivity problems within the network.",
  "done": true,
  "done_reason": "stop",
  "context": [
    128006,
    9125,
    128007,
    271,
    38766,
    1303,
    33025,
    2696,
    25,
    6790,
    220,
    2366,
    18,
    271,
    128009,
    128006,
    882,
    128007,
    271,
    9370,
    5730,
    553,
    420,
    1567,
    25,
    432,
    17,
    706,
    17162,
    1109,
    1403,
    8797,
    97639,
    37,
    85,
    17,
    19228,
    13,
    128009,
    128006,
    78191,
    128007,
    271,
    4599,
    459,
    432,
    17,
    320,
    25730,
    23570,
    220,
    17,
    8,
    3756,
    6821,
    330,
    71830,
    261,
    1109,
    1403,
    8797,
    97639,
    37,
    85,
    17,
    19228,
    498,
    433,
    3445,
    430,
    279,
    9457,
    374,
    12153,
    311,
    5813,
    477,
    10519,
    264,
    2539,
    74949,
    449,
    520,
    3325,
    1403,
    1023,
    97639,
    37,
    85,
    17,
    19228,
    382,
    3204,
    20280,
    85,
    17,
    320,
    5109,
    10928,
    478,
    8092,
    5629,
    2373,
    220,
    17,
    8,
    374,
    264,
    30158,
    11766,
    1511,
    369,
    958,
    46223,
    30946,
    1887,
    17320,
    13,
    362,
    8797,
    97639,
    37,
    85,
    17,
    9760,
    374,
    2631,
    369,
    279,
    9457,
    311,
    11322,
    23669,
    30158,
    323,
    4009,
    45982,
    18841,
    382,
    644,
    420,
    15398,
    11,
    432,
    17,
    1253,
    387,
    25051,
    832,
    315,
    279,
    2768,
    4819,
    1473,
    16,
    13,
    3146,
    89209,
    74949,
    8060,
    96618,
    578,
    9457,
    1253,
    539,
    617,
    1027,
    3025,
    311,
    5813,
    459,
    74949,
    449,
    520,
    3325,
    1403,
    19228,
    4245,
    311,
    6683,
    6103,
    11,
    6996,
    315,
    31357,
    11,
    477,
    1023,
    29130,
    4819,
    627,
    17,
    13,
    3146,
    43,
    474,
    315,
    97639,
    37,
    85,
    17,
    11766,
    7431,
    479,
    96618,
    3861,
    477,
    810,
    42617,
    60275,
    2643,
    539,
    387,
    20336,
    311,
    1629,
    97639,
    37,
    85,
    17,
    11,
    14718,
    279,
    432,
    17,
    3756,
    311,
    539,
    617,
    264,
    2539,
    743,
    315,
    19228,
    627,
    18,
    13,
    3146,
    12600,
    45982,
    9669,
    96618,
    578,
    4009,
    45982,
    2643,
    387,
    1778,
    430,
    433,
    596,
    5107,
    369,
    279,
    9457,
    311,
    5813,
    5361,
    2539,
    97639,
    37,
    85,
    17,
    12751,
    582,
    6072,
    382,
    1271,
    9006,
    420,
    4360,
    11,
    499,
    1053,
    11383,
    1205,
    311,
    1473,
    16,
    13,
    26504,
    323,
    4495,
    904,
    6683,
    6103,
    627,
    17,
    13,
    4343,
    4009,
    31357,
    323,
    6106,
    430,
    682,
    42617,
    60275,
    527,
    69384,
    627,
    18,
    13,
    28295,
    279,
    97639,
    37,
    85,
    17,
    11766,
    5110,
    389,
    832,
    477,
    810,
    42617,
    60275,
    422,
    5995,
    627,
    19,
    13,
    33180,
    349,
    323,
    2686,
    904,
    16940,
    4009,
    45982,
    4819,
    382,
    2746,
    2163,
    653,
    5102,
    291,
    11,
    420,
    4360,
    1253,
    1121,
    304,
    1207,
    2985,
    2931,
    30158,
    5178,
    323,
    4754,
    31357,
    5435,
    2949,
    279,
    4009,
    13
  ],
  "total_duration": 7397596583,
  "load_duration": 1681888375,
  "prompt_eval_count": 44,
  "prompt_eval_duration": 340486333,
  "eval_count": 314,
  "eval_duration": 5287706039
}
 amir@Amirmahdis-MacBook-Pro  ~  


  amir@Amirmahdis-MacBook-Pro  ~  curl -s http://127.0.0.1:11434/api/embed \
>   -H "Content-Type: application/json" \
>   -d '{
>     "model": "nomic-embed-text",
>     "input": "OSPF adjacency changed from Full to Deleted on VLAN 440."
>   }' | jq '.model, (.embeddings[0] | length)'
"nomic-embed-text"
768
 amir@Amirmahdis-MacBook-Pro  ~  


 amir@Amirmahdis-MacBook-Pro  ~  curl -s http://127.0.0.1:11434/api/chat \
>   -H "Content-Type: application/json" \
>   -d '{"model":"qwen2.5-coder:7b-instruct","messages":[]}' | jq
ollama ps
{
  "model": "qwen2.5-coder:7b-instruct",
  "created_at": "2026-08-05T18:15:56.222027Z",
  "message": {
    "role": "assistant",
    "content": ""
  },
  "done": true,
  "done_reason": "load"
}
 amir@Amirmahdis-MacBook-Pro  ~  ollama ps
NAME                         ID              SIZE      PROCESSOR    CONTEXT    UNTIL              
qwen2.5-coder:7b-instruct    dae161e27b0e    8.2 GB    100% GPU     32768      4 minutes from now    
 amir@Amirmahdis-MacBook-Pro  ~  


Host management-ollama-tunnel
    HostName 10.99.0.66
    User etu
    Port 22
    ProxyJump r1

    RemoteForward 11434 127.0.0.1:11434
    ExitOnForwardFailure yes
    ServerAliveInterval 30
    ServerAliveCountMax 3

ssh -N management-ollama-tunnel

 etu@management  ~  curl -s http://127.0.0.1:11434/api/version | jq
{
  "version": "0.24.0"
}
 etu@management  ~  


  etu@management  ~  ss -ltnp 2>/dev/null | grep 11434 || sudo ss -ltnp | grep 11434
LISTEN 0      128        127.0.0.1:11434      0.0.0.0:*   
LISTEN 0      128            [::1]:11434         [::]:*   
 etu@management  ~  


 etu@management  ~  curl -s http://127.0.0.1:11434/api/version | jq
curl -s http://127.0.0.1:11434/api/tags | jq '.models[].name'
{
  "version": "0.24.0"
}
"llama3.2:3b"
"nomic-embed-text:latest"
"qwen2.5-coder:7b-instruct"
"qwen3.5:9b-mlx"
 etu@management  ~  


  etu@management  ~  curl -s http://127.0.0.1:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "stream": false,
    "messages": [
      {"role": "user", "content": "Reply with exactly: phase5 remote ollama ok"}
    ]
  }' | jq -r '.message.content'
phase5 remote ollama ok
 etu@management  ~  
