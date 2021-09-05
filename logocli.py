import argparse
import cv2
import sys
import random
import numpy as np


def insert_logo_in_image(image, logo, placement="topleft", logoBackground=255):
    """
    :param image: Image to put a Logo on
    :param logo: Logo image to put on an Image (must be smaller than Image )
    :param logoBackground: 0 for Dark Background in Logo Image
                          255 for light Background in Logo Image
    :return: Image with Logo on Top Left Corner

    """

    rows, cols, channels = logo.shape

    if placement == "topleft":
        roi_xRange = slice(0, rows) #saving of index [0:rows]
        roi_yRange = slice(0, cols)
    elif placement == "bottomleft":
        roi_xRange = slice(image.shape[0]-rows, image.shape[0])
        roi_yRange = slice(0, cols)
    elif placement == "topright":
        roi_xRange = slice(0, rows)
        roi_yRange = slice(image.shape[1]-cols, image.shape[1])
    elif placement == "bottomright":
        roi_xRange = slice(image.shape[0]-rows, image.shape[0])
        roi_yRange = slice(image.shape[1]-cols, image.shape[1])
    else:
        sys.exit("Logo position was not defined properly")

    roi = image[roi_xRange, roi_yRange]

    # Now create a mask of logo and create its inverse mask also
    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)

    ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    mask_inv = cv2.bitwise_not(mask)

    # Now black-out the area of logo in ROI
    if logoBackground == 0:
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv) # Set roi Background to original Background outside mask
        img2_fg = cv2.bitwise_and(logo, logo, mask=mask) # Copy mask values to image foreground
    elif logoBackground == 255: # Or otherwise, if background is white
        img1_bg = cv2.bitwise_and(roi, roi, mask=mask)
        img2_fg = cv2.bitwise_and(logo, logo, mask=mask_inv)
    else:
        sys.exit("logoBackground not defined properly")

    # Put logo in ROI and modify the main image
    dst = cv2.add(img1_bg, img2_fg)

    output_image = image.copy()
    output_image[roi_xRange, roi_yRange] = dst
    return output_image


def get_inputmage_message():
    message = 'path to the Image that has to be processed. No quotation marks required.'
    return message


def get_addlogo_message():
    message = 'Logo File to include to the given input image. No quotation marks required.'
    return message


def get_logoposition_message():
    message = 'Where should the logo be located? Possible options: ' \
              'topleft, ' \
              'topright, ' \
              'bottomleft or ' \
              'bottomright. ' \
              'If not specified, topleft will be used'
    return message


def get_output_message():
    message = 'Name of the generated Image for example: ImageWithLogo.png. ' \
              'If no output name is specified, output.png will be used'
    return message


def get_background_message():
    message = 'specifies which background color lies under logo. Options: black, white.' \
              ' If no background is specified, white will be used'
    return message


if __name__ == '__main__':

    # Parser object to access input flags
    parser = argparse.ArgumentParser(description='CommandLine to insert a small logo into an Image '
                                                 'with filtering the background of the logo image')

    parser.add_argument('--inputImage', type=str, help=get_inputmage_message())
    parser.add_argument('--logoImage', type=str, help=get_addlogo_message())
    parser.add_argument('--logoPosition', type=str,
                        help=get_logoposition_message(), default='topleft')
    parser.add_argument('--outputFilename', type=str,
                        help=get_output_message(), default='output.png')
    parser.add_argument('--background', type=str, help=get_background_message())

    args = parser.parse_args()

    # Input Error Handling... minimum setup requires input and logo
    if args.inputImage is None:
        sys.exit("no input image specified. Try -h flag for help.")

    if args.logoImage is None:
        sys.exit("no logo image specified. Try -h flag for help.")

    # Renaming for easier handling
    inputName = args.inputImage
    outputName = args.outputFilename
    backgroundOption = args.background
    logoName = args.logoImage
    logoPosition = args.logoPosition

    # Read files
    inputAsImage = cv2.imread(inputName)
    logoAsImage = cv2.imread(logoName)

    # Default value for background
    bg_color = 255
    if backgroundOption == "black":
        bg_color = 0

    # Apply Method
    outputImg = insert_logo_in_image(inputAsImage, logoAsImage, logoPosition, bg_color)

    # Write to output
    cv2.imwrite(outputName, outputImg)


