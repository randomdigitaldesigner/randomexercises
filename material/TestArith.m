%--------------------------------------------------------------------------
%
%                               UTN - FRBA
%                    Diseño Digita con Logica programable
%                               Año: 2020
%
%--------------------------------------------------------------------------
%
% Autor: Martinez Garbino, Luio Jose
% Fecha: 
%
% Descripcion: ejemplos de metodos de redondeo y aritmetica en Punto Fijo
%
%--------------------------------------------------------------------------

clc
clear all
close all

a = 1.5
b = 2.5


disp(sprintf('  floor: %.1f: %d',a,floor(a)))
disp(sprintf('  floor: %.1f: %d',-a,floor(-a)))


disp(sprintf('  ceil: %.1f: %d',a,ceil(a)))
disp(sprintf('  ceil: %.1f: %d',-a,ceil(-a)))



disp(sprintf('  Nearest: %.1f: %d',a,nearest(a)))
disp(sprintf('  Nearest: %.1f: %d',-a,nearest(-a)))

disp(sprintf('  Nearest: %.1f: %d',b,nearest(b)))
disp(sprintf('  Nearest: %.1f: %d',-b,nearest(-b)))


disp(sprintf('  Round: %.1f: %d',a,round(a)))
disp(sprintf('  Round: %.1f: %d',-a,round(-a)))

disp(sprintf('  Round: %.1f: %d',b,round(b)))
disp(sprintf('  Round: %.1f: %d',-b,round(-b)))


disp(sprintf('  Fix: %.1f: %d',a,fix(a)))
disp(sprintf('  Fix: %.1f: %d',-a,fix(-a)))

disp(sprintf('  Fix: %.1f: %d',b,fix(b)))
disp(sprintf('  Fix: %.1f: %d',-b,fix(-b)))


disp(sprintf('  Convergent: %.1f: %d',a,convergent(a)))
disp(sprintf('  Convergent: %.1f: %d',-a,convergent(-a)))

disp(sprintf('  Convergent: %.1f: %d',b,convergent(b)))
disp(sprintf('  Convergent: %.1f: %d',-b,convergent(-b)))


afp = fi(a, 1, 8, 3)
bfp = fi(b, 1, 8, 3)

c = afp + bfp

d = afp * bfp



x0fp = fi(a, 1, 12, 4)  
x1fp = fi(b, 1, 8, 7)


%[8.4] +[1.7] = [Max(8,1)+1 .Max(4,7) ]=[9.7]=16
ys = x0fp + x1fp


%[8.4] *[1.7] = [8+1 . 4+7 ]=[9.11]=20
yp =x0fp * x1fp



