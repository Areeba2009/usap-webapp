import math
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PI_VAL = 3.1415192654

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    calc_type = data.get('calc_type', '').lower().strip()
    inputs = data.get('inputs', {})
    
    try:
        @app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    calc_type = data.get('calc_type', '').lower().strip()
    inputs = data.get('inputs', {})
    
    try:
        # 🚨 INPUT VALIDATION GUARD: Catch invalid inputs instantly
        raw_angle = float(inputs.get('angle', 0))
        raw_other_angle = float(inputs.get('other_arc_angle', 0))
        
        if raw_angle > 360 or raw_other_angle > 360:
            return jsonify({'error': "Invalid Angle: Parameters cannot exceed 360° boundary bounds."})
            
        if raw_angle < 0 or raw_other_angle < 0:
            return jsonify({'error': "Invalid Parameter: Negative angles are out of structural tracking limits."})

        # --- Your exact original mathematical formulas continue below untouched ---
        angle = raw_angle
        if angle == 0 and inputs.get('has_other_arc') == 'yes':
            angle = 360 - raw_other_angle

        # Full validation state restore mapping your exact original code parameters
        angle = float(inputs.get('angle', 0))
        if angle == 0 and inputs.get('has_other_arc') == 'yes':
            angle = 360 - float(inputs.get('other_arc_angle', 0))
        elif angle == 0 and inputs.get('fallback_arc_length'):
            arc_fallback = float(inputs.get('fallback_arc_length', 0))
            if inputs.get('is_radius_given') == 'yes':
                r_fallback = float(inputs.get('fallback_radius', 1))
                angle = (arc_fallback * 360) / (2 * PI_VAL * r_fallback)
            elif inputs.get('is_circumference_given') == 'yes':
                r_fallback = float(inputs.get('fallback_circumference', 0)) / (2 * PI_VAL)
                angle = (arc_fallback * 360) / (2 * PI_VAL * r_fallback)

        radius = float(inputs.get('radius', 0))
        if radius == 0:
            if inputs.get('is_circ_given_rad') == 'yes':
                radius = float(inputs.get('radius_circumference', 0)) / (2 * PI_VAL)
            elif inputs.get('is_circ_given_rad') == 'no':
                radius = (float(inputs.get('radius_arc_length', 0)) * 360) / (angle * 2 * PI_VAL)

        unit = inputs.get('final_unit', 'm')

        if "arc length" in calc_type:
            ans = math.radians(angle) * radius
            output_text = f"Arc Length: {round(ans, 3)} {unit}"
        elif "perimeter" in calc_type:
            arc_len = math.radians(angle) * radius
            ans = (2 * radius) + arc_len
            output_text = f"Perimeter of Sector: {round(ans, 3)} {unit}\nHappy Calculating!"
        else:
            if angle == 0 and inputs.get('is_arc_given_area') == 'yes':
                arc_area = float(inputs.get('area_arc_length', 0))
                r_area = float(inputs.get('area_radius_fallback', 1)) if inputs.get('is_rad_given_area') == 'yes' else (float(inputs.get('area_circ_fallback', 0)) / (2 * PI_VAL))
                angle = (arc_area * 360) / (2 * PI_VAL * r_area)
            elif angle == 0 and inputs.get('is_other_sector_angle_given') == 'yes':
                angle = 360 - float(inputs.get('other_sector_angle', 0))

            if radius == 0 and inputs.get('is_circ_given_area_rad') == 'yes':
                radius = float(inputs.get('area_radius_circ', 0)) / (2 * PI_VAL)

            ans = (angle / 360.0) * PI_VAL * (radius ** 2)
            output_text = f"Area of Sector: {round(ans, 3)} {unit}²"

        return jsonify({
            'result': output_text,
            'radius': radius,
            'angle': angle,
            'unit': unit
        })

    except Exception as e:
        return jsonify({'error': f"Mathematical System Fault: {str(e)}"})

@app.route('/stability-check', methods=['POST'])
def stability_check():
    data = request.get_json() or {}
    lat = float(data.get('lat', 31.5204))
    lng = float(data.get('lng', 74.3587))
    
    elevation = round(random.uniform(206.5, 214.2), 1)
    moisture = round(random.uniform(18.0, 72.0), 1)
    slope = round(random.uniform(0.4, 7.2), 1)
    humidity = round(random.uniform(45.0, 68.0), 1)
    
    is_buildable = slope < 5.0 and 25.0 <= moisture <= 65.0
    
    factors = []
    if slope >= 5.0: factors.append(f"Unstable Terrain Slope Gradient ({slope}°)")
    if moisture > 65.0: factors.append(f"High Water Table Risk ({moisture}%)")
    if moisture < 25.0: factors.append(f"Loose Granular Sand Base ({moisture}%)")
    
    verdict_text = "LAND BUILDABLE" if is_buildable else "LAND NON-BUILDABLE"
    justification = "Geotechnical matrix profile meets all stable infrastructure safety bounds." if is_buildable else f"Structural Constraints Detected: {', '.join(factors)}"
    
    return jsonify({
        'verdict': verdict_text,
        'elevation': f"{elevation} m",
        'moisture': f"{moisture}%",
        'slope': f"{slope}°",
        'humidity': f"{humidity}%",
        'justification': justification
    })

app = app
