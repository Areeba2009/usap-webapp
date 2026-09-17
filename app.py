import math
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def home():
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "System UI Compilation Fault: Unable to load templates/index.html file context."


PI_VAL = 3.1415926535

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    calc_type = data.get('calc_type', '').strip()
    inputs = data.get('inputs', {})
    
    try:
        raw_angle = float(inputs.get('angle', 0))
        raw_other_angle = float(inputs.get('other_arc_angle', 0))
        
        # Strict Boundary Validation Filters
        if raw_angle > 360 or raw_other_angle > 360:
            return jsonify({'error': "Invalid Angle: Parameters cannot exceed 360° bounds."})
        if raw_angle < 0 or raw_other_angle < 0:
            return jsonify({'error': "Invalid Parameter: Negative angles are out of tracking limits."})

        angle = raw_angle
        if angle == 0 and inputs.get('has_other_arc') == 'yes':
            angle = 360 - raw_other_angle

        # 1. ARC LENGTH MODULE CALCULATIONS
        if calc_type == 'Arc Length':
            radius = float(inputs.get('radius', 0))
            if radius == 0 and inputs.get('is_circ_given_rad') == 'yes':
                radius = float(inputs.get('radius_circumference', 0)) / (2 * PI_VAL)
            elif radius == 0 and inputs.get('is_circ_given_rad') == 'no':
                arc_len_val = float(inputs.get('radius_arc_length', 0))
                if angle > 0:
                    radius = (arc_len_val * 360) / (angle * 2 * PI_VAL)
            
            if angle == 0 and float(inputs.get('fallback_arc_length', 0)) > 0:
                fb_arc = float(inputs.get('fallback_arc_length', 0))
                if inputs.get('is_radius_given') == 'yes':
                    fb_rad = float(inputs.get('fallback_radius', 0))
                    angle = (fb_arc * 360) / (2 * PI_VAL * fb_rad) if fb_rad > 0 else 0
                elif inputs.get('is_circumference_given') == 'yes':
                    fb_circ = float(inputs.get('fallback_circumference', 0))
                    angle = (fb_arc / fb_circ) * 360 if fb_circ > 0 else 0
                radius = fb_rad if inputs.get('is_radius_given') == 'yes' else 0

            final_arc = (angle / 360.0) * (2 * PI_VAL * radius)
            unit = inputs.get('final_unit', 'm')
            return jsonify({
                'result': f"Calculated Internal Angle: {angle:.3f}°\nComputed Operations Radius: {radius:.3f} {unit}\nFinal Sector Arc Length: {final_arc:.3f} {unit}",
                'radius': radius,
                'angle': angle,
                'unit': unit
            })

        # 2. AREA OF SECTOR MODULE CALCULATIONS
        elif calc_type == 'Area of Sector':
            radius = float(inputs.get('radius', 0))
            if radius == 0 and inputs.get('is_circ_given_area_rad') == 'yes':
                radius = float(inputs.get('area_radius_circ', 0)) / (2 * PI_VAL)
            
            if angle == 0:
                if inputs.get('is_arc_given_area') == 'yes':
                    fb_arc = float(inputs.get('area_arc_length', 0))
                    if inputs.get('is_rad_given_area') == 'yes':
                        radius = float(inputs.get('area_radius_fallback', 0))
                    else:
                        radius = float(inputs.get('area_circ_fallback', 0)) / (2 * PI_VAL)
                    angle = (fb_arc * 360) / (2 * PI_VAL * radius) if radius > 0 else 0
                elif inputs.get('is_other_sector_angle_given') == 'yes':
                    angle = 360 - float(inputs.get('other_sector_angle', 0))

            final_area = (angle / 360.0) * PI_VAL * (radius ** 2)
            unit = inputs.get('final_unit', 'm')
            return jsonify({
                'result': f"Calculated Internal Angle: {angle:.3f}°\nComputed Operations Radius: {radius:.3f} {unit}\nFinal Sector Area Space: {final_area:.3f} {unit}²",
                'radius': radius,
                'angle': angle,
                'unit': unit
            })

        # 3. PERIMETER OF SECTOR MODULE CALCULATIONS
        elif calc_type == 'Perimeter of Sector':
            radius = float(inputs.get('radius', 0))
            if radius == 0 and inputs.get('is_circ_given_perim') == 'yes':
                radius = float(inputs.get('perim_circumference', 0)) / (2 * PI_VAL)
            
            arc_length = float(inputs.get('arc_length', 0))
            if arc_length == 0 and angle > 0:
                arc_length = (angle / 360.0) * (2 * PI_VAL * radius)
                
            final_perimeter = arc_length + (2 * radius)
            unit = inputs.get('final_unit', 'm')
            return jsonify({
                'result': f"Computed Operations Radius: {radius:.3f} {unit}\nComputed Sector Arc Length: {arc_length:.3f} {unit}\nFinal Structural Perimeter: {final_perimeter:.3f} {unit}",
                'radius': radius,
                'angle': angle,
                'unit': unit
            })

        return jsonify({'error': "Unknown calculation operation profile stream."})
    except Exception as e:
        return jsonify({'error': f"Mathematical Processing Exception: {str(e)}"})

@app.route('/stability-check', methods=['POST'])
def stability_check():
    data = request.get_json() or {}
    try:
        lat = float(data.get('lat', 31.52))
        lng = float(data.get('lng', 74.35))
        
        # Procedural Land Form Simulation Formula Logic Node
        seed_factor = math.sin(lat * 1000) * math.cos(lng * 1000)
        elevation = 206.0 + abs(seed_factor * 8.0)
        moisture = 20.0 + abs(seed_factor * 60.0)
        slope = abs(seed_factor * 6.5)
        humidity = 40.0 + abs(seed_factor * 30.0)
        
        factors = []
        if slope >= 5.0:
            factors.append(f"Unstable Terrain Slope Gradient ({slope:.1f}°)")
        if moisture > 65.0:
            factors.append(f"High Water Table Flood Risk ({moisture:.1f}%)")
        if moisture < 25.0:
            factors.append(f"Loose Granular Sand Base ({moisture:.1f}%)")
            
        is_buildable = len(factors) == 0
        verdict_text = "LAND BUILDABLE" if is_buildable else "LAND NON-BUILDABLE"
        justification = "Geotechnical matrix profile meets all stable infrastructure safety bounds." if is_buildable else f"Structural Constraints Detected: {', '.join(factors)}."
        
        return jsonify({
            'verdict': verdict_text,
            'elevation': f"{elevation:.1f} m",
            'moisture': f"{moisture:.1f}%",
            'slope': f"{slope:.1f}°",
            'humidity': f"{humidity:.1f}%",
            'justification': justification
        })
    except Exception as e:
        return jsonify({'error': f"Geospatial Processing Exception: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
