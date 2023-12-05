class Arithmetic {
add:
param x
param y
return x+y
subtract:
param x
param y
return x-y
multiply:
param x
param y
return x*y
divide:
param x
param y
if not y==0 goto _l1
call abort
_l1:
_t0 = x / y
res = _t0
goto _l0
_l0:
_l2:
if not x goto _l5
_t1 = y / x
res = _t1
goto _l2
_l5:
return res
}