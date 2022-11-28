#include <stdio.h>
#include <unistd.h>

void	write_hex(unsigned long address);
void	write_digit(short digit);

int main(void)
{
	int c;
	unsigned long address;

	address = (unsigned long)&c;
	
	printf("%p\n", &c);
	printf("%lx\n", address);

	write_hex(address);
}

void	write_hex(unsigned long address)
{
	if (address < 16)
		write_digit(address & 0xf);
	else
	{
		write_hex(address >> 4);
		write_digit(address & 0xf);
	}	
}

void	write_digit(short digit)
{
	write(1, &"0123456789abcdef"[digit], 1);
}
