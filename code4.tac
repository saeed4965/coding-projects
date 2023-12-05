class BooleanIfWhile {
declare a
b = true
method1:
_l0:
if not 10<30 goto _l3
_t0 = 1 + 5
_t1 = 10 * 2
_t2 = _t0 - _t1
a = _t2
goto _l0
_l3:
if not b goto _l5
c = 3
a = 2
_l5:
a = 3
goto _l4
_l4:
return a
}
class Main {
main:
return self
}