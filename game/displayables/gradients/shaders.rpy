init python:
    renpy.register_shader("2DVfx.simple_gradient", variables="""
    
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