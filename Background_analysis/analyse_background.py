#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 15:01:22 2022

Analyse des background du commissioning et de l'ERS MIRI CORONO

@author: cperrot
"""

import numpy as np
import matplotlib.pyplot as plt
import imodex_miri_postprocess_pipeline as imp #homemade pipeline
from scipy import ndimage
from scipy.optimize import curve_fit
from astropy.stats import sigma_clip

def bkg_log10(x,a,b):
    """Y = A + B * log10(x)"""
    return a+b*np.log10(x)




#definition of the path

path_raw_comm  = "/home/cperrot/Work/raw/JWST/Target/Comm/"
path_raw_ers  = "/home/cperrot/Work/raw/JWST/Target/ERS/"
path_code = "/home/cperrot/Work/code/JWST/Target/GTO/"
path_save = "/home/cperrot/Work/projet/JWST/Target/GTO/Bkg_analyse/"

#background de 1140C

folder="1140C/"

#comm 1045
prop="1045"
bkg_1=path_raw_comm+prop+"/jw0"+prop+f"{48:03}"+"001_02101_"+f"{1:05}"+"_mirimage/"
bkg_2=path_raw_comm+prop+"/jw0"+prop+f"{65:03}"+"001_02101_"+f"{1:05}"+"_mirimage/"
bkg_3=path_raw_comm+prop+"/jw0"+prop+f"{65:03}"+"001_02101_"+f"{2:05}"+"_mirimage/"
bkg_4=path_raw_comm+prop+"/jw0"+prop+f"{65:03}"+"001_02101_"+f"{3:05}"+"_mirimage/"
bkg_5=path_raw_comm+prop+"/jw0"+prop+f"{65:03}"+"001_02101_"+f"{4:05}"+"_mirimage/"
bkg_6=path_raw_comm+prop+"/jw0"+prop+f"{81:03}"+"001_02101_"+f"{1:05}"+"_mirimage/"
prop="HIP65426"
bkg_7=path_raw_ers+prop+"/obs28_COR_F1140C/"
bkg_8=path_raw_ers+prop+"/obs29_COR_F1140C/"
bkg_9=path_raw_ers+prop+"/obs34_COR_F1140C/"
bkg_10=path_raw_ers+prop+"/obs35_COR_F1140C/"




img1, head1 = imp.load_cube(bkg_1, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img2, head2 = imp.load_cube(bkg_2, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img3, head3 = imp.load_cube(bkg_3, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img4, head4 = imp.load_cube(bkg_4, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img5, head5 = imp.load_cube(bkg_5, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img6, head6 = imp.load_cube(bkg_6, "rateints", xdim=200, ydim=200, x0=120, y0=112)
tmp, head7 = imp.load_cube(bkg_7, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img7 = tmp[0,:,:,:]
img8 = tmp[1,:,:,:]
tmp, head8 = imp.load_cube(bkg_8, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img9 = tmp[0,:,:,:]
img10 = tmp[1,:,:,:]
'''
tmp, head9 = imp.load_cube(bkg_9, "rate", xdim=200, ydim=200, x0=120, y0=112)
img11 = tmp[0,:,:,:]
img12 = tmp[1,:,:,:]
tmp, head10 = imp.load_cube(bkg_10, "rate", xdim=200, ydim=200, x0=120, y0=112)
img13 = tmp[0,:,:,:]
img14 = tmp[1,:,:,:]
'''
print("1: "+str(img1.shape))
print("2: "+str(img2.shape))
print("3: "+str(img3.shape))
print("4: "+str(img4.shape))
print("5: "+str(img5.shape))
print("6: "+str(img6.shape))
print("7: "+str(img7.shape))
print("8: "+str(img8.shape))
print("9: "+str(img9.shape))
print("10: "+str(img10.shape))
'''
print("11: "+str(img11.shape))
print("12: "+str(img12.shape))
print("13: "+str(img13.shape))
print("14: "+str(img14.shape))
'''
label = ["Obs 48", "Obs 65 - 1", "Obs 65 - 2", "Obs 65 - 3", "Obs 65 - 4", "Obs 81", "Obs 28 - 1", "Obs 28 - 2", "Obs 29 - 1", "Obs 29 - 2"]#, "Obs 34 - 1", "Obs 34 - 2", "Obs 35 - 1", "Obs 35 - 2"]
img = [img1, img2, img3, img4, img5, img6, img7, img8, img9, img10]#, img11, img12, img13, img14]

dx=10
q1=[100+dx, -1, 0, 100-dx]
q2=[100+dx, -1, 100+dx, -1]
q3=[0, 100-dx, 0, 100-dx]
q4=[0, 100-dx,100+dx, -1]
qn=[q1,q2,q3,q4]
fcolor=['blue','orange','green','red','purple','brown','pink','grey', 'olive', 'cyan','black','yellow','indigo','darkblue']
qname = ['Quadran Upper Left','Quadran Upper Right', 'Quadran Lower Left','Quadran Lower Right']

#MEDIAN
for j in range(4):
	fig=plt.figure()
	for i in range(len(img)):
		med  = np.median(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]],axis=(1,2))
		mean = np.mean(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]],axis=(1,2))
		plt.plot(med,'D',color=fcolor[i],ms=2,mew=1.25,markerfacecolor='None')
		plt.plot(med,color=fcolor[i],label=label[i])
		medfull = np.median(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]])
		plt.plot([-1,100],[medfull,medfull],'--',color=fcolor[i],lw=1)
	
	plt.ylabel('ADU',fontsize=10)
	plt.xlabel('Integration number',fontsize=10)
	plt.legend(loc='upper right',fontsize='x-small')
	plt.ylim([4,9])
	plt.xlim([-0.5,41])
	plt.grid()
	plt.title(qname[j]+" Median")
	fig.tight_layout()
	fig.savefig(path_save+folder+'median_bkg_'+qname[j]+'F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
	plt.close(fig)
	
	
	
	
for j in range(4):
	fig=plt.figure()
	for i in range(len(img)):
		stdd = np.std(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]],axis=(1,2))
		plt.plot(stdd,'D',color=fcolor[i],ms=2,mew=1.25,markerfacecolor='None')
		plt.plot(stdd,color=fcolor[i],label=label[i])
	
	plt.ylabel('ADU',fontsize=10)
	plt.xlabel('Integration number',fontsize=10)
	plt.legend(loc='upper right',fontsize='x-small')
	plt.ylim([0,2.5])
	plt.grid()
	plt.title(qname[j]+" Std dev")
	fig.tight_layout()
	fig.savefig(path_save+folder+'Std_dev_bkg_'+qname[j]+'F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
	plt.close(fig)

dx=10
mask=np.zeros((200,200))+1.
mask[100-dx:100+dx,:]=0
mask[:,100-dx:100+dx]=0

vmin=0
vmax=6
fig1,[[sub1,sub2],[sub3,sub4]] = plt.subplots(nrows=2,ncols=2,figsize=(6.1,8))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
tmp1 = sub1.imshow(img1[1,100+dx:,0:100-dx],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,100-dx,100+dx,200])
tmp2 = sub2.imshow(img1[1,100+dx:,100+dx:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[100+dx,200,100+dx,200])
tmp3 = sub3.imshow(img1[1,0:100-dx,0:100-dx],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,100-dx,0,100-dx])
tmp4 = sub4.imshow(img1[1,0:100-dx,100+dx:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[100+dx,200,0,100-dx])
sub2.get_yaxis().set_visible(False)
sub4.get_yaxis().set_visible(False)
sub1.get_xaxis().set_visible(False)
sub2.get_xaxis().set_visible(False)
cax  = fig1.add_axes([1, 0.12, 0.02, 0.75])
cbar = fig1.colorbar(tmp3, cax=cax, orientation='vertical')
cbar.set_label('ADU',fontsize=10)
cbar.ax.tick_params(length=2,pad=1,labelsize=10)
fig1.savefig(path_save+folder+'bkg_4quadran_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig1)









dx = 15
gs = [0,200,100-dx,100+dx]

medimg1=np.median(img8[1:,:,:],axis=0)
#medimg1=img1[3,:,:] #pas de median
vmin=3
vmax=6.5
fig1 = plt.figure()
plt.imshow(medimg1[100-dx:100+dx,0:200],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,200,100-dx,100+dx])
#plt.imshow(img1[1,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)#,extent=gs)
fig1.savefig(path_save+folder+'glow_stick_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig1)

dx = 5
mask_croix = np.zeros((220,220))#+1.
mask_croix[:,110-dx:110+dx] = 1
mask_croix[110-dx:110+dx,:] = 1
xdeg=4.5
maskgs=ndimage.rotate(mask_croix,xdeg,reshape=False)
maskgs[np.where(maskgs >= 0.5)] = 1
maskgs[np.where(maskgs < 0.5)] = 0
#maskgs_inv= maskgs*(-1.)+1.
maskgs_inv = maskgs[10:210,10:210] < 1

vmin=4
vmax=8
fig1 = plt.figure()
plt.imshow(maskgs_inv*medimg1,origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,200,0,200])
fig1.savefig(path_save+folder+'mask_glow_stick_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig1)



med_masked = maskgs_inv*medimg1
res = np.zeros((200,200))
deg_poly = 2
#median_verticale
for i in range(200):
	tmp = med_masked[:,i]
	tmp_mask = maskgs_inv[:,i]
	#popt, pcov = curve_fit(bkg_log10, range(200), tmp, p0=[np.median(tmp[0:10]), 0.5])
	#fit = bkg_log10(range(200),popt[0],popt[1])
	#res[:,i] = fit
	res[:,i] = np.median(sigma_clip(tmp[tmp_mask], sigma=2, masked=False)) #np.median(tmp) ### faire un sigma clipping poru virer les pixel chaud
	#z = np.poly1d(np.polyfit(range(200),tmp,deg_poly))
	#res[:,i] = z(range(200))

#median_horizontale
med_masked = maskgs_inv*(medimg1-res)
resh = np.zeros((200,200))
for i in range(200):
	tmp = med_masked[i,:]
	tmp_mask = maskgs_inv[i,:]
	#popt, pcov = curve_fit(bkg_log10, range(200), tmp, p0=[np.median(tmp[0:10]), 0.5])
	#fit = bkg_log10(range(200),popt[0],popt[1])
	#res[:,i] = fit
	resh[i,:] = np.median(sigma_clip(tmp[tmp_mask], sigma=2, masked=False)) #np.median(tmp) ### faire un sigma clipping poru virer les pixel chaud
	#z = np.poly1d(np.polyfit(range(200),tmp,deg_poly))
	#res[:,i] = z(range(200))
resh=0

vmin=4
vmax=8
fig,[sub1,sub2,sub3] = plt.subplots(nrows=1,ncols=3,figsize=(10,4))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
tmp1 = sub1.imshow(medimg1,origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,200,0,200])
tmp2 = sub2.imshow(res+resh,origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,200,0,200])
tmp3 = sub3.imshow(medimg1-(res+resh),origin='lower',cmap='seismic',interpolation='none',vmin=-0.5,vmax=.5,extent=[0,200,0,200])
sub1.get_yaxis().set_visible(False)
sub2.get_yaxis().set_visible(False)
sub3.get_yaxis().set_visible(False)
sub1.get_xaxis().set_visible(False)
sub2.get_xaxis().set_visible(False)
sub3.get_xaxis().set_visible(False)
cax1  = fig.add_axes([0.01, 0.076, 0.305, 0.035])
cbar = fig.colorbar(tmp1, cax=cax1, orientation='horizontal')
cax2  = fig.add_axes([0.349, 0.076, 0.305, 0.035])
cbar = fig.colorbar(tmp2, cax=cax2, orientation='horizontal')
cax3  = fig.add_axes([0.688, 0.076, 0.305, 0.035])
cbar = fig.colorbar(tmp3, cax=cax3, orientation='horizontal')
cbar.set_label('ADU',fontsize=10)
cbar.ax.tick_params(length=2,pad=1,labelsize=10)
fig.savefig(path_save+folder+'bkg_data_model_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)

### fitter un polynome sur les colonnes de l'image pour interpoler le bkg sur le GS
### retirer le fit polynomiale pour n'avoir que le GS


fig = plt.figure()
for i in [2,92,150]:
	plt.plot(range(200),medimg1[:,i],lw=0.5,color=fcolor[i%8])
	plt.plot(range(200),res[:,i],'--',lw=0.5,color=fcolor[i%8])
	plt.ylabel('ADU')
	plt.xlabel('Vertical axis')
	plt.xlim([-1,201])
	plt.ylim([4,7])
fig.savefig(path_save+folder+'Vertical_axis_cut.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)

fig = plt.figure()
for i in [2,100,150]:
	plt.plot(range(200),res[:,i],lw=0.5)
	plt.ylabel('ADU')
	plt.xlabel('Vertical axis')
	plt.xlim([-1,201])
	plt.ylim([0,8])
fig.savefig(path_save+folder+'Vertical_axis_cut_fit.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)

















#### PLOT DES IMAGES DE BKG


#OBS 48
vmin=3
vmax=6
fig, axs = plt.subplots(2,5, figsize=(12, 6))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(10):
	axs[i].imshow(img1[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'bkg_obs_48_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)


#OBS 65 - 1
vmin=3
vmax=6
fig, axs = plt.subplots(3,7, figsize=(12, 6))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(21):
	axs[i].imshow(img2[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'bkg_obs_65_1_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)


#OBS 81
vmin=3
vmax=6
fig, axs = plt.subplots(3,7, figsize=(12, 6))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(21):
	axs[i].imshow(img6[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'bkg_obs_81_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)


#OBS 28 - 1
vmin=4
vmax=7
fig, axs = plt.subplots(5,8, figsize=(8, 6))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(40):
	axs[i].imshow(img7[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
#plt.axis('off')
fig.savefig(path_save+folder+'bkg_obs_28_1_F1140_Comm_ERS.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)







######################## ERS





folder="ERS_HIP_1140C/"

#comm 1045
prop="1386"

filtre="F1550C"#"F1140C"

prop="HIP65426"
rol_1=path_raw_ers+prop+"/obs5_COR_F1140C/"
rol_2=path_raw_ers+prop+"/obs4_COR_F1140C/"
ref_1=path_raw_ers+prop+"/obs6_COR_F1140C/"
bkg_1=path_raw_ers+prop+"/obs28_COR_F1140C/"
bkg_2=path_raw_ers+prop+"/obs29_COR_F1140C/"

rol_1=path_raw_ers+prop+"/obs8_COR_F1550C/"
rol_2=path_raw_ers+prop+"/obs9_COR_F1550C/"
ref_1=path_raw_ers+prop+"/obs7_COR_F1550C/"
bkg_1=path_raw_ers+prop+"/obs30_COR_F1550C/"
bkg_2=path_raw_ers+prop+"/obs31_COR_F1550C/"



img1, head1 = imp.load_cube(rol_1, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img2, head2 = imp.load_cube(rol_2, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img3, head3 = imp.load_cube(ref_1, "rateints", xdim=200, ydim=200, x0=120, y0=112)
tmp, head4 = imp.load_cube(bkg_1, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img4 = tmp[0,:,:,:]
img5 = tmp[1,:,:,:]
tmp, head6 = imp.load_cube(bkg_2, "rateints", xdim=200, ydim=200, x0=120, y0=112)
img6 = tmp[0,:,:,:]
img7 = tmp[1,:,:,:]


deuxadeux = img1-img4

print("1: "+str(img1.shape))
print("2: "+str(img2.shape))
print("3: "+str(img3.shape))
print("4: "+str(img4.shape))
print("5: "+str(img5.shape))
print("6: "+str(img6.shape))
print("7: "+str(img7.shape))

### median of the ref dithering

img33 = np.median(img3,axis=0)

label = ["Roll 1", "Roll 2", "Ref", "Bkg Roll 1", "Bkg Roll 2", "Bkg Ref 1", "Bkg Ref 2"]
img = [img1, img2, img33, img4, img5, img6, img7]

dx=10
q1=[100+dx, -1, 0, 100-dx]
q2=[100+dx, -1, 100+dx, -1]
q3=[0, 100-dx, 0, 100-dx]
q4=[0, 100-dx,100+dx, -1]
qn=[q1,q2,q3,q4]
fcolor=['blue','orange','green','red','purple','brown','pink','grey', 'olive', 'cyan','black','yellow','indigo','darkblue']
qname = ['Quadran Upper Left','Quadran Upper Right', 'Quadran Lower Left','Quadran Lower Right']





#MEDIAN
for j in range(4):
	fig=plt.figure()
	for i in range(len(img)):
		med  = np.median(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]],axis=(1,2))
		mean = np.mean(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]],axis=(1,2))
		plt.plot(med,'D',color=fcolor[i],ms=2,mew=1.25,markerfacecolor='None')
		plt.plot(med,color=fcolor[i],label=label[i])
		medfull = np.median(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]])
		plt.plot([-1,100],[medfull,medfull],'--',color=fcolor[i],lw=1)
	
	plt.ylabel('ADU',fontsize=10)
	plt.xlabel('Integration number',fontsize=10)
	plt.legend(loc='upper right',fontsize='x-small')
	if filtre == 'F1140C':
		plt.ylim([5,9])
		plt.xlim([-0.5,41])
	if filtre == 'F1550C':
		plt.ylim([6.5,11])
		plt.xlim([-0.5,60])
	plt.grid()
	plt.title(qname[j]+" Median")
	fig.tight_layout()
	fig.savefig(path_save+folder+'median_bkg_'+qname[j]+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
	plt.close(fig)

# STD DEV
for j in range(4):
	fig=plt.figure()
	for i in range(len(img)):
		stdd = np.std(img[i][:,qn[j][0]:qn[j][1],qn[j][2]:qn[j][3]],axis=(1,2))
		plt.plot(stdd,'D',color=fcolor[i],ms=2,mew=1.25,markerfacecolor='None')
		plt.plot(stdd,color=fcolor[i],label=label[i])
	
	plt.ylabel('ADU',fontsize=10)
	plt.xlabel('Integration number',fontsize=10)
	plt.legend(loc='upper right',fontsize='x-small')
	if filtre == 'F1140C':
		plt.ylim([0.5,2.5])
	if filtre == 'F1550C':
		plt.ylim([0.75,2.])	
	plt.grid()
	plt.title(qname[j]+" Std dev")
	fig.tight_layout()
	fig.savefig(path_save+folder+'Std_dev_bkg_'+qname[j]+'F1140_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
	plt.close(fig)


dx=10
mask=np.zeros((200,200))+1.
mask[100-dx:100+dx,:]=0
mask[:,100-dx:100+dx]=0

vmin=0
vmax=8
fig1,[[sub1,sub2],[sub3,sub4]] = plt.subplots(nrows=2,ncols=2,figsize=(6.1,8))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
tmp1 = sub1.imshow(img1[1,100+dx:,0:100-dx],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,100-dx,100+dx,200])
tmp2 = sub2.imshow(img1[1,100+dx:,100+dx:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[100+dx,200,100+dx,200])
tmp3 = sub3.imshow(img1[1,0:100-dx,0:100-dx],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[0,100-dx,0,100-dx])
tmp4 = sub4.imshow(img1[1,0:100-dx,100+dx:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax,extent=[100+dx,200,0,100-dx])
sub2.get_yaxis().set_visible(False)
sub4.get_yaxis().set_visible(False)
sub1.get_xaxis().set_visible(False)
sub2.get_xaxis().set_visible(False)
cax  = fig1.add_axes([1, 0.12, 0.02, 0.75])
cbar = fig1.colorbar(tmp3, cax=cax, orientation='vertical')
cbar.set_label('ADU',fontsize=10)
cbar.ax.tick_params(length=2,pad=1,labelsize=10)
fig1.savefig(path_save+folder+'bkg_4quadran_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig1)


#### PLOT DES IMAGES DE BKG


# ROLL 1
vmin=0
vmax=8
fig, axs = plt.subplots(6,10, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(60):
	axs[i].imshow(img1[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'roll_1_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)

# ROLL 2
vmin=0
vmax=8
fig, axs = plt.subplots(6,10, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(60):
	axs[i].imshow(img2[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'roll_2_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)


# BKG REF 1
vmin=0
vmax=9
fig, axs = plt.subplots(4,5, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(19):
	axs[i].imshow(img3[0,i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'ref_1_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)



# BKG ROLL 1
vmin=0
vmax=8
fig, axs = plt.subplots(6,10, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(60):
	axs[i].imshow(img4[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'bkg_roll_1_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)

# BKG ROLL 2
vmin=0
vmax=8
fig, axs = plt.subplots(6,10, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(60):
	axs[i].imshow(img5[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'bkg_roll_2_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)





# BKG REF 1
vmin=0
vmax=9
fig, axs = plt.subplots(4,5, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(19):
	axs[i].imshow(img6[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'bkg_ref_1_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)

# BKG REF 2
vmin=0
vmax=9
fig, axs = plt.subplots(4,5, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(19):
	axs[i].imshow(img7[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'bkg_ref_2_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)




# BKG ROLL 2
vmin=-1
vmax=1
fig, axs = plt.subplots(6,10, figsize=(12, 10))
plt.subplots_adjust(wspace=0.12, hspace=0.05, left=0.01, right=0.99)
axs = axs.ravel()
for i in range(60):
	axs[i].imshow(deuxadeux[i,:,:],origin='lower',cmap='inferno',interpolation='none',vmin=vmin,vmax=vmax)
	axs[i].get_yaxis().set_visible(False)
	axs[i].get_xaxis().set_visible(False)
fig.savefig(path_save+folder+'deux_a_deux_'+filtre+'_ERS_'+prop+'.pdf',format='pdf',bbox_inches='tight')
plt.close(fig)








#imp.plot_image(img1[2,:,:],path_save+"bkg_1.pdf",vmin='',vmax='',dim=200,cmap='inferno', title="no",xlab="",ylab="")