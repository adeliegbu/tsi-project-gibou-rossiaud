#version 330 core

layout(location = 0) in vec3 in_pos;
layout(location = 1) in vec3 in_norm;
layout(location = 2) in vec3 in_color;
layout(location = 3) in vec2 in_uv;

uniform mat4 translation;
uniform mat4 rotation;
uniform mat4 projection;

out vec3 frag_color;

void main() {
    gl_Position = projection * translation * rotation * vec4(in_pos, 1.0);
    frag_color = in_color;
}
