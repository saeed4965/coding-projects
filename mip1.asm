.data

.text
li $t0, 2
sw $t0, main_x
lw $t0, main_"hello"
sw $t0, main_y
li $v0, 1
jr $ra
li $v0, param1
jr $ra
li $v0, 0
jr $ra
jr $ra