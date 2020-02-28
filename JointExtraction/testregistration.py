#!/usr/bin/env python

from __future__ import print_function
from functools import reduce


import SimpleITK as sitk
import sys
import os


def command_iteration(method) :
    print("{0:3} = {1:7.5f} : {2}".format(method.GetOptimizerIteration(),
                                           method.GetMetricValue(),
                                           method.GetOptimizerPosition()))


pixelType = sitk.sitkFloat32

fixed = sitk.ReadImage('t4.jpg', sitk.sitkFloat32)
fixed = sitk.Normalize(fixed)
fixed = sitk.DiscreteGaussian(fixed, 2.0)


moving = sitk.ReadImage('t3.jpg', sitk.sitkFloat32)
moving = sitk.Normalize(moving)
moving = sitk.DiscreteGaussian(moving, 2.0)


R = sitk.ImageRegistrationMethod()

R.SetMetricAsJointHistogramMutualInformation()

R.SetOptimizerAsGradientDescentLineSearch(learningRate=1.0,
                                          numberOfIterations=200,
                                          convergenceMinimumValue=1e-5,
                                          convergenceWindowSize=5)

R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))

R.SetInterpolator(sitk.sitkLinear)

R.AddCommand( sitk.sitkIterationEvent, lambda: command_iteration(R) )

outTx = R.Execute(fixed, moving)

print("-------")
print(outTx)
print("Optimizer stop condition: {0}".format(R.GetOptimizerStopConditionDescription()))
print(" Iteration: {0}".format(R.GetOptimizerIteration()))
print(" Metric value: {0}".format(R.GetMetricValue()))


sitk.WriteTransform(outTx,  'outTx.tfm')

import numpy as np

if ( not "SITK_NOSHOW" in os.environ ):

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(fixed)
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetDefaultPixelValue(1)
    resampler.SetTransform(outTx)

    out = resampler.Execute(moving)

    simg1 = sitk.Cast(sitk.RescaleIntensity(fixed), sitk.sitkUInt8)
    simg2 = sitk.Cast(sitk.RescaleIntensity(out), sitk.sitkUInt8)
    cimg = sitk.Compose(simg1, simg2, simg1//2.+simg2//2.)

    fixed_numpy = sitk.GetArrayFromImage(fixed)
    moving_numpy = sitk.GetArrayFromImage(moving)
    result_numpy = sitk.GetArrayFromImage(out)

    from matplotlib import pyplot as plt

    f, axarr = plt.subplots(2,2)
    axarr[0,0].imshow(fixed_numpy)
    axarr[0,1].imshow(moving_numpy)
    axarr[1,0].imshow(result_numpy)
    plt.show()

   #plt.imshow(out_as_numpy, interpolation='nearest')
   # plt.show()

  #  sitk.WriteImage(out, 'out.png')
   # sitk.Show( cimg, "ImageRegistration2 Composition" )