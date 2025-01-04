init python:
    renpy.register_shader("2DVfx.rawcircle", variables="""
        
        uniform float u_radius;
        uniform vec2 u_center;
        uniform vec3 u_color;

        attribute vec4 a_position;
        varying vec2 v_position;

        """,vertex_300="""
        
        v_position = a_position.xy;

        """, fragment_300="""
        vec2 pos = v_position - vec2(u_radius, u_radius);
        float dist = distance(pos, u_center);

        if (dist <= u_radius) {
            gl_FragColor = vec4(u_color, 1.0);

        }""")

    renpy.register_shader("2DVfx.circle", variables="""

        uniform float u_alias_factor; // Anti-aliasign factor.
        uniform float u_radius;
        uniform vec2 u_center;
        uniform vec3 u_color;

        attribute vec4 a_position;
        varying vec2 v_position;

        """, vertex_300="""
        
        v_position = a_position.xy;

        """, fragment_300="""
        vec2 pos = v_position - vec2(u_radius, u_radius);
        float dist = distance(pos, u_center);
        float alpha = smoothstep(u_radius, u_radius - u_alias_factor, dist);

        if (dist <= u_radius) {
            gl_FragColor = mix(vec4(0.0), vec4(u_color, 1.0), alpha);
            
        } else {
            gl_FragColor = vec4(0.0);

        }""")
    
    renpy.register_shader("2DVfx.hollowcircle", variables="""

        uniform float u_alias_factor; // Anti-aliasign factor.
        uniform float u_thickness;    // How thick the border is.
        uniform float u_radius;
        uniform vec2 u_center;
        uniform vec3 u_color;

        attribute vec4 a_position;
        varying vec2 v_position;

        """, vertex_300="""
        
        v_position = a_position.xy;

        """, fragment_300="""
        vec2 pos = v_position - vec2(u_radius, u_radius);
        float dist = distance(pos, u_center);

        float inner_radius = u_radius - u_thickness;
        float alpha_outer = smoothstep(u_radius, u_radius - u_alias_factor, dist);
        float alpha_inner = 0.0;

        if (u_thickness < u_radius) {
            alpha_inner = smoothstep(inner_radius + u_alias_factor, inner_radius, dist);
        }

        if (dist <= u_radius && dist >= inner_radius) {
            float alpha = alpha_outer * (1.0 - alpha_inner) + alpha_inner * (1.0 - alpha_outer);
            gl_FragColor = mix(vec4(0.0), vec4(u_color, 1.0), alpha);
            
        } else {
            gl_FragColor = vec4(0.0);

        }""")
    
    renpy.register_shader("2DVfx.hollowarc", variables="""

        uniform float u_alias_factor;
        uniform float u_thickness;
        uniform float u_progress;
        uniform float u_rotation;
        uniform float u_radius;
        uniform vec2 u_center;
        uniform vec3 u_color;

        attribute vec4 a_position;
        varying vec2 v_position;

        """, vertex_300="""
        
        v_position = a_position.xy;

        """, fragment_300="""
        vec2 pos = v_position - vec2(u_radius, u_radius);
        float dist = distance(pos, u_center);
        float pi = 3.14159265359;

        float inner_radius = u_radius - u_thickness;

        float angle = atan(pos.y - u_center.y, pos.x - u_center.x);
        float norm_angle = 1.0 - (angle + pi) / (2.0 * pi);
        norm_angle = mod(norm_angle + u_rotation, 1.0);

        float alpha_outer = smoothstep(u_radius, u_radius - u_alias_factor, dist);
        float alpha_inner = 0.0;

        if (u_thickness < u_radius) {
            alpha_inner = smoothstep(inner_radius + u_alias_factor, inner_radius, dist);
        }

        float alpha = alpha_outer * (1.0 - alpha_inner) + 
                    alpha_inner * smoothstep(inner_radius, inner_radius - u_alias_factor, dist);

        float progress_start = 0.0;
        float progress_end = u_progress;

        bool in_arc = false;
        if (u_progress == 0.0) {
            in_arc = false;
            
        } else if (progress_end > progress_start) {
            in_arc = (norm_angle >= progress_start && norm_angle <= progress_end);
        
        } else {
            in_arc = (norm_angle >= progress_start || norm_angle <= progress_end);

        }

        bool valid_arc = false;
        
        if (u_thickness == u_radius) {
            valid_arc = (dist <= u_radius && in_arc);

        } else {
            valid_arc = (dist <= u_radius && dist >= inner_radius && in_arc);
        
        }

        if (valid_arc) {
            gl_FragColor = mix(vec4(0.0), vec4(u_color, 1.0), alpha);
            
        } else {
            gl_FragColor = vec4(0.0); 

        }""")