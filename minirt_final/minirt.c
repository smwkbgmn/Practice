/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   minirt.c                                           :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: donghyu2 <donghyu2@student.42seoul.kr>     +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2023/11/01 21:54:32 by donghyu2          #+#    #+#             */
/*   Updated: 2024/01/25 11:24:32 by donghyu2         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

// Implement cylinder
// Add one more object > Cone
// Test min, max of point and sclar value

// Remove function not allowed
// See including headers
// Check diameter

// Camera at 0,0,0 error
// Inside object specular
// Correct camera calculating

#include "minirt.h"

void	print_data(t_render *data);

int	main(int argc, char *argv[])
{
	t_render	data;
	
	if (argc == 2)
	{
		init(argv[1], &data);
		print_data(&data);
		render(&data);
	}
	else if (argc == 1)
		err_usr("please enter a file for rendering");
	else
		err_usr("only a file is allowed");

	return (EXIT_SUCCESS);
}
