from flask import Flask, render_template, url_for, request
import os
from IAI_Control import *
from valve import *

#Home the robot, then move to the center of the cracker.
initialize()
IAI_Robot_Move('absolute', 'xyz', 0.3, 100, 100, 70, 80)

app = Flask(__name__)
drawn_strokes = [] # Store strokes drawn by the user
    
@app.route('/', methods=['POST', 'GET'])
def index():
    # Render the main page and pass any drawn strokes
    return render_template('index.html', strokes=drawn_strokes)
    
@app.route('/run_preset/<int:preset_id>', methods=['GET'])
def run_preset(preset_id):
    # Run a preset pattern based on the selected preset ID
    if preset_id == 1:
        return function1()
    elif preset_id == 2:
        return function2()
    elif preset_id == 3:
        return function3()
    elif preset_id == 4:
        return function4()
    elif preset_id == 5:
        return function5()
    else:
        return {"error": "Invalid preset"}

# Define functions for each preset pattern

def function1():
    #Draw a boat shape
    IAI_Draw_Boat(30, 100, 70)
    return {"message": "Function 1 executed"}

def function2():
    #Draw a smiley face shape
    IAI_Draw_Smile_Face(30, 100, 70)
    return {"message": "Function 2 executed"}

def function3():
    #Draw a snowe flake shape
    IAI_Draw_Flake(30, 100, 70)
    return {"message": "Function 3 executed"}

def function4():
    #Draw a star shape
    IAI_Draw_Star(25, 100, 70)
    return {"message": "Function 4 executed"}

def function5():
    #Draw an umbrella shape
    IAI_Draw_Umbrella(30, 100, 70)
    return {"message": "Function 5 executed"}

    
scale_factor = 0.15 # Scale factor for strokes (turn 400px by 400px canvas to 60px by 60px)

@app.route('/print_strokes', methods=['POST'])
def print_strokes():
    # Receive and process strokes drawn by the user
    if request.method == 'POST':
        all_strokes = request.get_json()
        for stroke in all_strokes:
            lst_stroke = []
            for pos in stroke:
                x = pos['x']
                y = pos['y']

                if (x,y) not in lst_stroke:
                    lst_stroke.append((x*scale_factor,y*scale_factor))

            drawn_strokes.append(lst_stroke)
        if len(drawn_strokes) > 0:    
            IAI_Free_Draw(100,70,drawn_strokes)
        return 'OK'

@app.route('/clear_strokes', methods=['POST'])
def clear_strokes():
    # Clear the stored strokes
    global drawn_strokes
    if request.method == 'POST':
        drawn_strokes = []
        return 'OK'

if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True,
            host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))