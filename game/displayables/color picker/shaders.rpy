init python:
    renpy.register_shader("2DVfx.square_gradient", variables="""
    
        uniform vec4 u_bottom_right;
        uniform vec4 u_bottom_left;
        uniform vec4 u_top_right;
        uniform vec4 u_top_left;

        attribute vec4 a_tex_coord;
        varying vec4 v_tex_coord;

        """, vertex_300="""

        v_tex_coord = a_tex_coord;

        """, fragment_300="""
        vec2 uv = v_tex_coord.xy;

        vec3 back = mix(u_top_left.rgb, u_top_right.rgb, uv.x);
        vec3 front = mix(u_bottom_left.rgb, u_bottom_right.rgb, uv.x);
        vec3 end = mix(back, front, uv.y);

        gl_FragColor = vec4(end, 1.0);""")

    renpy.register_shader("2DVfx.spectrum_gradient", variables="""

        uniform float u_angle;
        attribute vec2 a_tex_coord;
        varying vec2 v_tex_coord;

        """, fragment_functions="""

        vec3 hls2rgb(float h, float s, float l) {
            float hp = h / 60.0;
            float c = (1.0 - abs(2.0 * l - 1.0)) * s;
            float m = l - c/2.0;
            float x = c * (1.0 - abs(mod(hp, 2.0) - 1.0));

            vec3 rgb;

            if (hp <= 1.0) {
                rgb = vec3(c, x, 0.0);
            
            } else if (hp <= 2.0) {
                rgb = vec3(x, c, 0.0);
            
            } else if (hp <= 3.0) {
                rgb = vec3(0.0, c, x);
            
            } else if (hp <= 4.0) {
                rgb = vec3(0.0, x, c);

            } else if (hp <= 5.0) {
                rgb = vec3(x, 0.0, c);

            } else {
                rgb = vec3(c, 0.0, x);
            }

            return rgb + m;
        }

        """, vertex_300="""

        v_tex_coord = a_tex_coord.xy;

        """, fragment_300="""
        float t;

        if (u_angle != 0.0) {
            t = v_tex_coord.y;
        
        } else {
            t = v_tex_coord.x;}

        float hue = t * 360.0;

        float sat = 1.0;
        float light = 0.5;

        vec3 color = hls2rgb(hue, sat, light);

        gl_FragColor = vec4(color, 1.0);""")