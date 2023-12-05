DOG_age: .space 4
DOG_color: .space 4
main_dog1: .space 4
.data

.text
lw $t0, DOG_"Hola"
sw $t0, DOG_bark
li $t0, 5
sw $t0, DOG_age
lw $t0, DOG_"black"
sw $t0, DOG_color
lw $t0, DOG_radius
sw $t0, DOG__t0
lw $t0, DOG__t0
sw $t0, DOG_xddd
jr $ra
jal dog1_init
jr $ra