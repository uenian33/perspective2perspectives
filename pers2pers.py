import os
import cv2 
import lib.Equirec2Perspec as E2P
import lib.Perspec2Equirec as P2E
import lib.multi_Perspec2Equirec as m_P2E
import glob
import argparse




def equir2pers(eq_im,
               FOV=120,
               theta=0,
               phi=0,
               height=1280,
               width=1280): # Specify parameters(FOV, theta, phi, height, width)

    #
    # FOV unit is degree
    # theta is z-axis angle(right direction is positive, left direction is negative)
    # phi is y-axis angle(up direction positive, down direction negative)
    # height and width is output image dimension
    #
    
    #input_img = './panorama/world_map.jpeg'
    #output_dir = './example/perspective'
    #if not os.path.exists(output_dir):
    #    os.mkdir(output_dir)
    
    equ = E2P.Equirectangular(eq_im)    # Load equirectangular image

    pers_im = equ.GetPerspective(FOV, theta, phi, height, width)
    
    return pers_im


def pers2equir(im, FOV=120, 
               theta=0,
               phi=0):
    #
    # FOV unit is degree
    # theta is z-axis angle(right direction is positive, left direction is negative)
    # phi is y-axis angle(up direction positive, down direction negative)
    # height and width is output image dimension
    #
   
    # this can turn cube to panorama
    equ = m_P2E.Perspective([im],
                            [[FOV, theta, phi]])    
    
    
    eq_im, eq_mask = equ.GetEquirec(height,width)  
    #print(eq_mask)
    return eq_im, eq_mask



if __name__ == '__main__':
    # convert equarectangular to perspective
    input_img = './panorama/world_map.jpeg'
    input_img = cv2.imread(input_img, cv2.IMREAD_COLOR)
    
    equ = E2P.Equirectangular(input_img)    # Load equirectangular image

    pers_im = equ.GetPerspective(90, 0, 0, 640, 640)  # Specify parameters(FOV, theta, phi, height, width)
    cv2.imwrite('eq2pers.png', pers_im)


    # convert one perspective to another
    #input_dir = './example/perspective'

    width = 1920
    height = 960

    
    #input1 = input_dir + '/perspective_1.png' # 90, 0, 0
    #input2 = input_dir + '/perspective_2.png' # 120, 0, 90

    im1 = cv2.imread('eq2pers.png', cv2.IMREAD_COLOR)
    eq, eq_mask = pers2equir(im1, FOV=90, 
			       theta=0,
			       phi=0)

    new_pers = equir2pers(eq,
                           FOV=90,
                           theta=90,
                           phi=0,)

    new_pers_mask = equir2pers(eq_mask,
                           FOV=90,
                           theta=90,
                           phi=0,)

    cv2.imwrite('pers2eq.png', eq)
    cv2.imwrite('pers2pers.png', new_pers)
    cv2.imwrite('pers2pers_mask.png', new_pers_mask)
    cv2.imwrite('pers2pers_eq_mask.png', eq_mask)

    
