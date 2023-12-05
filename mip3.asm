.data

.text
li $v0, x+y
jr $ra
li $v0, x-y
jr $ra
li $v0, x*y
jr $ra
lw $t0, Arithmetic_x
sw $t0, Arithmetic__t0
lw $t0, Arithmetic__t0
sw $t0, Arithmetic_res
lw $t0, Arithmetic_y
sw $t0, Arithmetic__t1
lw $t0, Arithmetic__t1
sw $t0, Arithmetic_res
li $v0, res
jr $ra