#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normale;
layout (location = 2) in vec3 color;
layout (location = 3) in vec2 texture;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;


out vec3 coordonnee_3d;
out vec3 coordonnee_3d_locale;
out vec3 vnormale;
out vec3 vColor;
out vec2 vTexture;

//Un Vertex Shader minimaliste
void main (void)
{
  //Les coordonnees 3D du sommet
  coordonnee_3d = position;

  //Coordonnees du sommet
  vec4 p = view*model*vec4(position, 1.0);
  coordonnee_3d_locale = p.xyz;

  //Projection du sommet
  p = projection*p;

  //Gestion des normales
  vec4 n = model*vec4(normale, 0.0);
  vnormale = n.xyz;

  //position dans l'espace ecran
  gl_Position = p;

  vTexture = texture;

  vColor = color;
}