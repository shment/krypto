import streamlit as st
import random
import base64

def expression_to_nums_ops(expression):
    ops = []
    ops_idx = [-1]
    nums = []
    for i, c in enumerate(expression):
        if c in ['+', '-', '*', ':']:
            ops.append(c)
            ops_idx.append(i)
            
    ops_idx.append(len(expression))
    for i in range(len(ops_idx) - 1):
        try:
            nums.append(int(expression[ops_idx[i] + 1: ops_idx[i + 1]]))
        except:
            return None
    
    if len(nums) - len(ops) != 1:
        return None
        
    return nums, ops


def nums_ops_to_res(nums, ops):
    k = 0
    while '*' in ops or ':' in ops:
        if ops[k] == '*':
            num = nums[k] * nums[k + 1]
            nums = nums[0: k] + [num] + nums[k + 2: ]
            ops.pop(k) 
            k = 0
        elif ops[k] == ':':
            num = nums[k] / nums[k + 1]          
            nums = nums[0: k] + [num] + nums[k + 2: ]
            ops.pop(k) 
            k = 0
        else:
            k += 1
    
    k = 0
    while '+' in ops or '-' in ops:
        if ops[k] == '+':
            num = nums[k] + nums[k + 1]
            nums = nums[0: k] + [num] + nums[k + 2: ]
            ops.pop(k) 
            k = 0
        elif ops[k] == '-':
            num = nums[k] - nums[k + 1]
            nums = nums[0: k] + [num] + nums[k + 2: ]
            ops.pop(k) 
            k = 0
        else:
            k += 1

    return nums[0]
        
   
def str_to_num(text):
    if '(' not in text:
        nums_ops = expression_to_nums_ops(text)
        if nums_ops is None:
            return None
        else:
            nums, ops = nums_ops
            res = nums_ops_to_res(nums, ops)
            return res
        
    inner_close = len(text)
    for i, c in enumerate(text):
        if c == ')':
            inner_close = i
            break
            
    inner_open = -1
    for i in range(inner_close):
        if text[inner_close - 1 - i] == '(':
            inner_open = inner_close - 1 - i
            break
        
    expression = text[inner_open + 1: inner_close]
    if len(expression) > 0:
        nums_ops = expression_to_nums_ops(expression)
        if nums_ops is None:
            return None
        else:
            nums, ops = nums_ops
            res = nums_ops_to_res(nums, ops)
    else:
        res = ''
    
    if inner_open == -1:
        inner_open = 0
    
    if inner_close == len(text):
        inner_close = len(text) - 1
        
    text = text[0: inner_open] + str(res) + text[inner_close + 1: ]
    return str_to_num(text)
    
    
def init_game():
    k = 0
    while k < 1000:
        k += 1
        try:
            possible_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            ops = []
            nums = []
            open_parenthesis = []
            close_parenthesis = []
            
            for i in range(5):
                num = random.choice(possible_nums)
                nums.append(num)
                possible_nums.remove(num)

            for i in range(4):
                ops.append(random.choice(['+', '-', '*', ':']))
            
            res = nums[0]
            for i in range(4):
                res = res + ops[i] + nums[i + 1]
                
            for i in range(4):
                j = random.randint(0, len(res) - 2)
                res = res[0: j] + '(' + res[j: ]
                
            for i in range(4):
                j = random.randint(1, len(res) - 1)
                res = res[0: j] + ')' + res[j: ]
            
            open_minus_close = 0
            for c in res:
                if c == '(':
                    open_minus_close += 1
                elif c == ')':
                    open_minus_close -= 1    
                
                if open_minus_close < 0:
                    break 
            
            if open_minus_close >= 0:      
                if str_to_num(res) is not None:
                    objective = str_to_num(res)
                    if objective == int(objective) and objective > 0:
                        while '()' in res:
                            i = res.find('()')
                            res = res[0: i] + res[i + 2: ]

                        l = ['(1)', '(2)', '(3)', '(4)', '(5)', '(6)', '(7)', '(8)', '(9)']
                        for x in l:
                            while x in res:
                                i = res.find(x)
                                res = res[0: i] + res[i + 1] + res[i + 3: ]
                            
                        random.shuffle(nums)
                        return nums, int(objective), res
        except:
            pass

def numbers_to_text(nums):
    s = ''
    for num in nums:
        s = s + str(num) + ', '
        
    return s[0: -2]

def play_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

st.set_page_config(layout="wide")
st.subheader("Goal is to achieve the objective by using all 5 numbers, parenthesis and the 4 basic arithmetic operations. Example:")
st.code("numbers=5,2,3,1,4 objective=1")
st.code("((1+2)*3-4):5=1")
new_button = st.button('New Game')
if new_button:
    st.session_state.nums, st.session_state.objective, st.session_state.sol = init_game()
elif "nums" not in st.session_state or "objective" not in st.session_state:
    st.session_state.nums, st.session_state.objective, st.session_state.sol = init_game()
    
st.header("Numbers and Objective: " + numbers_to_text(st.session_state.nums) + "\t" + "->" + "\t" + str(int(st.session_state.objective)))
expression = st.text_input('Enter your answer here')
check_button = st.button('Check Solution')
sol_button = st.button('Show solution')
if sol_button:
    st.code(st.session_state.sol)
    
if check_button:
    res = str_to_num(expression)
    if res is None:
        st.error("Expression not valid")
    else:
        st.info("Your expression equal " + str(int(res)))
        nums_used = [x for x in expression if x in ['1', '2', '3', '4', '5', '6', '7', '8', '9']]
        if res == st.session_state.objective and set(nums_used) == set(st.session_state.nums):
            st.success("You did it!")
            play_audio("win.wav")
        else:
            st.error("Wrong result")
