BooleanIfWhile_a: .space 4
.data

.text
lw $t0, BooleanIfWhile_true
sw $t0, BooleanIfWhile_b
li $t0, 1
sw $t0, BooleanIfWhile__t0
li $t0, 10
sw $t0, BooleanIfWhile__t1
lw $t0, BooleanIfWhile__t0
sw $t0, BooleanIfWhile__t2
lw $t0, BooleanIfWhile__t2
sw $t0, BooleanIfWhile_a
li $t0, 3
sw $t0, BooleanIfWhile_c
li $t0, 2
sw $t0, BooleanIfWhile_a
li $t0, 3
sw $t0, BooleanIfWhile_a
li $v0, a
jr $ra
li $v0, self
jr $ra