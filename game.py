import streamlit as st
import random
import base64

def init_game():
    while True:
        possible_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ops = []
        nums = []

        for i in range(5):
            num = random.choice(possible_nums)
            nums.append(num)
            possible_nums.remove(num)

        for i in range(4):
            ops.append(random.choice(['+', '-', '*', ':']))

        res = nums[0]
        for i in range(4):
            if ops[i] == '+':
                res += nums[i + 1]
            if ops[i] == '-':
                res -= nums[i + 1]
            if ops[i] == '*':
                res *= nums[i + 1]
            if ops[i] == ':':
                res /= nums[i + 1]  

        if res == int(res) and res > 0:
            sol = '((((' + str(nums[0])
            for num, op in zip(nums[1: ], ops):
                sol = sol + op + str(num) + ')'
                
            random.shuffle(nums)
            return nums, int(res), sol

def numbers_to_text(nums):
    s = ''
    for num in nums:
        s = s + str(num) + ', '
        
    return s[0: -2]

def is_sol_legit():
    sol_nums = [st.session_state['num' + str(i + 1)] for i in range(5)]
    sol_nums.sort()
    st.session_state.nums.sort()
    for i in range(5):
        if sol_nums[i] != st.session_state.nums[i]:
            return False
    
    return True

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

st.write("The goal is to achieve the objective by using all 5 numbers and the 4 basic arithmetic operations.")
st.write("Operations order are performed as follows:")
st.code("((((num1 op1 num2) op2 num3) op3 num4) op4 num5)")
st.write("For example:")
st.code("num1=1, num2=2, num3=3, num4=4, num5=5, op1=+, op2=*, op3=-, op4=:")
st.code("((((1+2)*3)-4):5)=1")
new_button = st.button('New Game')
if new_button:
    st.session_state.nums, st.session_state.objective, st.session_state.sol = init_game()
elif "nums" not in st.session_state or "objective" not in st.session_state:
    st.session_state.nums, st.session_state.objective, st.session_state.sol = init_game()
st.header("Numbers are: " + numbers_to_text(st.session_state.nums))
st.header("Objective: " + str(st.session_state.objective))
cols = st.columns(9)
col_idx = 0
with cols[col_idx]:
    res = st.radio('num1', [1, 2, 3, 4, 5, 6, 7, 8, 9], key='num1')
    col_idx += 1

for i in range(4):
    with cols[col_idx]:
        op = st.radio('op' + str(i + 1), ['+', '-', '*', ':'], key='op' + str(i + 1))
        col_idx += 1
        
    with cols[col_idx]:
        num = st.radio('num' + str(i + 2), [1, 2, 3, 4, 5, 6, 7, 8, 9], key='num' + str(i + 2))
        
    if op == '+':
        res += num
    elif op == '-':
        res -= num
    elif op == '*':
        res *= num
    elif op == ':':
        res /= num
    
    with cols[col_idx]:
        st.write("res = " + str(res))
        col_idx += 1
        
sol_button = st.button('Show Solution')
if sol_button:
    st.header("Solution: " + st.session_state.sol)
    
if int(res) == st.session_state.objective and is_sol_legit():
    st.success("You did it !")
    play_audio("win.wav")
else:
    st.error("Wrong result")
