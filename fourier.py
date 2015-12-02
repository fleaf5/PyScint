import numpy as np
from scipy.fftpack import fftshift, fft2, ifft2, ifftshift, fft, ifft

def __init__():
    return 

def parabola(x,x0,y0):
    return -y0/x0**2.0*(x-x0)**2.0 + y0

def get_conjugate_spectrum(I):
    Ic = fftshift(fft2(I))
    return Ic

def convolved_conjugate_spectrum(Ic,xmin,xmax,ymin,ymax,x1,x2,y1,y2,doppler,delay):
    I = ifft2(ifftshift(Ic))

    yi = np.argmin(abs(delay-np.average([y1,y2])))
    xi = np.argmin(abs(doppler-np.average([x1,x2])))

    mask = np.zeros(Ic.shape)
    mask[xmin:xmax,ymin:ymax]=1.0
    for i in range(ymin,ymax):
        yu=parabola(doppler[i],x1,y1)
        yl=parabola(doppler[i],x2,y2)
        mask[:,i] = np.where(delay>yu, 0, mask[:,i])
        mask[:,i] = np.where(delay<yl, 0, mask[:,i])
    Iarc = ifft2(ifftshift(Ic*mask))
    I2 = np.real(I)*np.exp(-1.0j*np.angle(Iarc))
    I2c = fftshift(fft2(I2))
    I2c = np.roll(np.roll(I2c,xi-len(doppler)/2,1),yi-len(delay)/2,0)
    return I2c

def fourier_transform_incremental_width(I,frequency,f0):
    If = np.ones(I.shape)*(1.0 + 1.0j)
    next = 0.0
    for i in range(len(frequency)):
        #if i%len(frequency)>next:
        #    print str(next*100.) + ' % through at index ' + str(i)
        #    next += 0.1
        If[i,:] = slow_dft(I[i,:],frequency[i]/f0)
    Ic = fftshift(fft(If,axis=0))
    return Ic
    
def slow_dft(x,scaling):
    #x = np.asarray(x,dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N,1))
    k = np.where(k>len(k)/2,k-len(k),k)*scaling
    k = np.where(k<0,k+len(k),k)
    M = np.exp(-2j*np.pi*k*n/N)
    return np.dot(M,x)
