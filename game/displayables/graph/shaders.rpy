init python:
    renpy.register_shader("2DVfx.graph_segment", variables="""
    
        uniform float u_line_width;
        uniform vec2 u_model_size;
        uniform float u_alpha;
        uniform vec4 u_color;
        uniform float u_y;
        uniform float u_h;

        attribute vec4 a_tex_coord;
        varying vec4 v_tex_coord;

        """, vertex_300="""

        v_tex_coord = a_tex_coord;

        """, fragment_300="""
        
        vec2 norm = vec2(u_y, u_h) / u_model_size.y;
        vec2 st = v_tex_coord.xy;

        float height = mix(norm.x, norm.y, st.x);

        float shape_alias = 0.02;
        float line_alias = 0.01;
        float line_width = u_line_width / u_model_size.y;

        float line = smoothstep(
            1.0 - height - line_width - line_alias,
            1.0 - height - line_width, st.y
            ) * (1.0 - smoothstep(
            1.0 - height,
            1.0 - height + line_alias, st.y));

        float shape = smoothstep(
            1.0 - height - shape_alias,
            1.0 - height + shape_alias,
            st.y);

        float final_alpha = mix(shape * u_alpha, 1.0, line);

        gl_FragColor = u_color * final_alpha;

        """)
    
    renpy.register_shader("2DVfx.anim_graph_segment", variables="""
    
        uniform float u_line_width;
        uniform vec2 u_model_size;
        uniform float u_alpha;
        uniform vec4 u_start_color;
        uniform vec4 u_end_color;
        uniform float u_y;
        uniform float u_h;

        attribute vec4 a_tex_coord;
        varying vec4 v_tex_coord;

        """, vertex_300="""

        v_tex_coord = a_tex_coord;

        """, fragment_300="""
        
        vec2 norm = vec2(u_y, u_h) / u_model_size.y;
        vec2 st = v_tex_coord.xy;

        float height = mix(norm.x, norm.y, st.x);

        float shape_alias = 0.02;
        float line_alias = 0.01;
        float line_width = u_line_width / u_model_size.y;

        float line = smoothstep(
            1.0 - height - line_width - line_alias,
            1.0 - height - line_width, st.y
            ) * (1.0 - smoothstep(
            1.0 - height,
            1.0 - height + line_alias, st.y));

        float shape = smoothstep(
            1.0 - height - shape_alias,
            1.0 - height + shape_alias,
            st.y);

        vec3 color = mix(u_start_color.rgb, u_end_color.rgb, st.x);

        float final_alpha = mix(shape * u_alpha, 1.0, line);

        gl_FragColor = vec4(color, 1.0) * final_alpha;

        """)