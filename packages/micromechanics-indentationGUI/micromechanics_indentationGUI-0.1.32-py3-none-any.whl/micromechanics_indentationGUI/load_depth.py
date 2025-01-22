#pylint: disable=possibly-used-before-assignment, used-before-assignment

""" Graphical user interface to plot load-depth curves """
from micromechanics import indentation
import numpy as np
import matplotlib.pylab as plt
from PySide6.QtGui import QCursor, QAction, QKeySequence, QShortcut, QIcon # pylint: disable=no-name-in-module
from PySide6.QtWidgets import QMenu, QTableWidgetItem # pylint: disable=no-name-in-module
from .CorrectThermalDrift import correctThermalDrift


def set_aspectRatio(event_ax=None,ax=None,ratio=0.618):
  """
  set the aspect ratio of a matplotlib.figure

  Args:
    event_ax (class): the ax of a mtaplotlib.figure
    ax (class): the ax of a mtaplotlib.figure
    ratio (float): the aspect ratio
  """
  if ax is None:
    ax = event_ax
  else:
    ax.callbacks.connect('xlim_changed', set_aspectRatio)
    ax.callbacks.connect('ylim_changed', set_aspectRatio)
  x_left, x_right = ax.get_xlim()
  y_low, y_high = ax.get_ylim()
  ax.set_aspect(abs((x_right-x_left)/(y_low-y_high))*ratio)


def plot_load_depth(self,tabName,SimplePlot=False,If_inclusive_frameStiffness='inclusive'):
  """
  Graphical user interface to plot the load-depth curves of the chosen tests

  Args:
    tabName (string): the name of Tab Widget
    SimplePlot (bool): if true, this function will only plot the load-depht curve
    If_inclusive_frameStiffness (string): 'inclusive' or 'exclusive'
  """
  self.pars_plot_load_depth ={'plot_multiTest': False}
  #close all matplot figures before plotting new figures
  plt.close('all')
  #define indentation
  i = eval(f"self.i_{tabName}") # pylint: disable = eval-used
  #reset testList
  i.testList = list(i.allTestList)
  #read ax to plot load depth curves
  ax=eval(f"self.static_ax_load_depth_tab_{If_inclusive_frameStiffness}_frame_stiffness_{tabName}") # pylint: disable = eval-used
  ax[0].cla()
  ax[1].cla()
  #read static canvas
  static_canvas=eval(f"self.static_canvas_load_depth_tab_{If_inclusive_frameStiffness}_frame_stiffness_{tabName}") # pylint: disable = eval-used
  #read inputs from GUI
  selectedTests=eval(f"self.ui.tableWidget_{tabName}.selectedItems()") # pylint: disable = eval-used
  if If_inclusive_frameStiffness == 'inclusive':
    if SimplePlot:
      showDrift = False
      showFindSurface = False
      show_iLHU = False
    else:
      showDrift = eval(f"self.ui.checkBox_showThermalDrift_tab_{If_inclusive_frameStiffness}_frame_stiffness_{tabName}.isChecked()") # pylint: disable = eval-used
      showFindSurface = eval(f"self.ui.checkBox_showFindSurface_tab_{If_inclusive_frameStiffness}_frame_stiffness_{tabName}.isChecked()") # pylint: disable = eval-used # showFindSurface verifies plotting dP/dh slope
      show_iLHU=eval(f"self.ui.checkBox_iLHU_{If_inclusive_frameStiffness}_frame_stiffness_{tabName}.isChecked()") # pylint: disable = eval-used  #plot the load-depth curves of the seclected tests
  elif If_inclusive_frameStiffness == 'exclusive':
    showFindSurface = False
    show_iLHU = False
  #re-read the parameters for finding surface
  UsingRate2findSurface = eval(f"self.ui.checkBox_UsingRate2findSurface_{tabName}.isChecked()") # pylint: disable = eval-used
  Rate2findSurface = eval(f"self.ui.doubleSpinBox_Rate2findSurface_{tabName}.value()") # pylint: disable = eval-used
  DataFilterSize = eval(f"self.ui.spinBox_DataFilterSize_{tabName}.value()") # pylint: disable = eval-used
  if DataFilterSize%2==0:
    DataFilterSize+=1
  if UsingRate2findSurface:
    Surface = {"abs(dp/dh)": Rate2findSurface, "median filter": DataFilterSize}
    i.surface.update(Surface)
  #re-read the parameters for indentifing Loading-Holding-UnloadingStart-UnloadingEnd
  unloaPMax = eval(f"self.ui.doubleSpinBox_Start_Pmax_{tabName}.value()") # pylint: disable = eval-used
  unloaPMin = eval(f"self.ui.doubleSpinBox_End_Pmax_{tabName}.value()") # pylint: disable = eval-used
  relForceRateNoise = eval(f"self.ui.doubleSpinBox_relForceRateNoise_{tabName}.value()") # pylint: disable = eval-used
  max_size_fluctuation = eval(f"self.ui.spinBox_max_size_fluctuation_{tabName}.value()") # pylint: disable = eval-used
  Model = {"unloadPMax": unloaPMax, "unloadPMin": unloaPMin, "relForceRateNoise": relForceRateNoise, "maxSizeFluctuations": max_size_fluctuation}
  i.model.update(Model)
  plot_multiTest = False
  if len(selectedTests) > 1:
    plot_multiTest = True
  self.pars_plot_load_depth['plot_multiTest'] = plot_multiTest
  for j, Test in enumerate(selectedTests):
    column=Test.column()
    if column==0:  #Test Names are located at column 0
      i.testName=Test.text()
      if i.vendor == indentation.definitions.Vendor.Agilent:
        if show_iLHU and not plot_multiTest:
          i.output['ax'] = None
          i.output['plotLoadHoldUnload'] = True # plot iLHU
        i.nextAgilentTest(newTest=False)
        i.nextTest(newTest=False,plotSurface=(showFindSurface and not plot_multiTest))
        i.output['plotLoadHoldUnload'] = False
      if i.vendor == indentation.definitions.Vendor.Micromaterials:
        if show_iLHU and not plot_multiTest:
          i.output['ax'] = None
          i.output['plotLoadHoldUnload'] = True # plot iLHU
        i.nextMicromaterialsTest(newTest=False)
        i.nextTest(newTest=False,plotSurface=(showFindSurface and not plot_multiTest))
        i.output['plotLoadHoldUnload'] = False
      ax[0].set_title(f"{i.testName}")
      i.output['ax']=ax
      try:
        correctDrift = eval(f"self.ui.checkBox_UsingDriftUnloading_{tabName}.isChecked()") # pylint: disable = eval-used
      except:
        correctDrift = False
      if correctDrift and (If_inclusive_frameStiffness == 'inclusive'):
        ax_thermalDrift = False
        if showDrift and not plot_multiTest:
          fig_thermalDrift, ax_thermalDrift = plt.subplots()
        correctThermalDrift(indentation=i, ax=ax_thermalDrift, reFindSurface=True) #calibrate the thermal drift using the collection during the unloading
        if showDrift:
          try:
            fig_thermalDrift.legend()
            fig_thermalDrift.show()
          except Exception as e: #pylint: disable=broad-except
            suggestion = 'If you want to plot load-depth curves of more than 1 test, please do not check "show thermal drift"' #pylint: disable=anomalous-backslash-in-string
            self.show_error(str(e), suggestion)
      elif correctDrift:
        correctThermalDrift(indentation=i, reFindSurface=True) #calibrate the thermal drift using the collection during the unloading

      if If_inclusive_frameStiffness=='exclusive':
        i.h -= i.tip.compliance*i.p
      if i.method in (indentation.definitions.Method.ISO, indentation.definitions.Method.MULTI) and not plot_multiTest:
        i.stiffnessFromUnloading(i.p, i.h, plot=True)
        exec(f"self.indentation_inLoadDepth_{tabName} = i") # pylint: disable = exec-used
      elif i.method== indentation.definitions.Method.CSM or plot_multiTest:
        i.output['ax'][0].scatter(i.h, i.p, s=1, label=f"{i.testName}", picker=True)
        if j==len(selectedTests)-1:
          i.output['ax'][0].axhline(0, linestyle='-.', color='tab:orange', label='zero Load or Depth') #!!!!!!
          i.output['ax'][0].axvline(0, linestyle='-.', color='tab:orange') #!!!!!!
          if len(selectedTests)<=10: # show legend when the number of curves is smaller than 10
            i.output['ax'][0].legend()
          #pick the label of datapoints
          i.output['ax'][0].figure.canvas.mpl_connect("pick_event", pick)
          i.output['ax'][0].set_ylabel(r'force [$\mathrm{mN}$]')
          i.output['ax'][1].set_ylabel(r"$\frac{P_{cal}-P_{mea}}{P_{mea}}x100$ [%]")
          i.output['ax'][1].set_xlabel(r'depth [$\mathrm{\mu m}$]')
      i.output['ax']=None
  static_canvas.figure.set_tight_layout(True)
  static_canvas.draw()

def pick(event):
  """
  picking annotation

  Args:
    event (class): matplotlib event see: https://matplotlib.org/stable/users/explain/event_handling.html
  """
  global annot #pylint:disable=global-variable-undefined
  if event.mouseevent.button==1: # "1" is the left button
    try:
      annot.set_visible(False) #pylint:disable=used-before-assignment
    except:
      pass
    annot = event.mouseevent.inaxes.annotate("", xy=(0,0), xytext=(20,10),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"), #pylint:disable=use-dict-literal
                    arrowprops=dict(arrowstyle="->"))    #pylint:disable=use-dict-literal
    annot.set_visible(False)
    try:
      text = event.artist.get_label()
      print(text)
    except:
      pass
    else:
      annot.xy = [event.mouseevent.xdata, event.mouseevent.ydata]
      annot.set_text(text)
      annot.get_bbox_patch().set_facecolor('gray')
      annot.get_bbox_patch().set_alpha(0.4)
      annot.set_visible(True)
      event.mouseevent.canvas.draw_idle()

def setAsContactSurface(self):
  """
  set a data point selected by mouse as the contact surface
  """
  global annot #pylint:disable=global-variable-undefined
  event=self.matplotlib_event
  try:
    annot.set_visible(False) #pylint:disable=used-before-assignment
  except:
    pass
  annot = event.mouseevent.inaxes.annotate("", xy=(0,0), xytext=(-100,50),textcoords="offset points",
                  bbox=dict(boxstyle="round", fc="w"), #pylint:disable=use-dict-literal
                  arrowprops=dict(arrowstyle="->"))    #pylint:disable=use-dict-literal
  annot.set_visible(False)
  self.get_current_tab_name()
  tabName = self.get_current_tab_name()
  i = eval(f"self.indentation_inLoadDepth_{tabName}") #pylint:disable=eval-used
  index_Test = i.allTestList.index(i.testName)
  tableWidget = eval(f"self.ui.tableWidget_{tabName}") #pylint:disable=eval-used
  xdata = event.mouseevent.xdata
  ydata = event.mouseevent.ydata
  Distance = ((i.h*1000-xdata*1000)**2 + (i.p-ydata)**2)**0.5
  indexX = np.argmin(Distance)
  text = f"index {indexX} \nwas set as the contact surface\n of {i.testName}"
  annot.xy = [xdata, ydata]
  annot.set_text(text)
  annot.get_bbox_patch().set_facecolor('gray')
  annot.get_bbox_patch().set_alpha(0.4)
  annot.set_visible(True)
  event.mouseevent.canvas.draw_idle()
  #
  if tabName in ['tabTipRadius', 'tabPopIn']:
    tableWidget.setItem(index_Test,3,QTableWidgetItem(f"{indexX}"))
  else:
    tableWidget.setItem(index_Test,2,QTableWidgetItem(f"{indexX}"))

def right_click_set_ContactSurface(self, event):
  """
  picking annotation

  Args:
    event (class): matplotlib event see: https://matplotlib.org/stable/users/explain/event_handling.html
  """
  if not self.pars_plot_load_depth['plot_multiTest']:
    if event.mouseevent.button == 3:       #"3" is the right button
      #I create the context menu
      self.popMenu = QMenu(self)
      Action_setAsContactSurface = QAction("Set as the contact surface", self)
      self.matplotlib_event = event
      Action_setAsContactSurface.triggered.connect(self.setAsContactSurface)
      self.popMenu.addAction(Action_setAsContactSurface)
      cursor = QCursor()
      self.popMenu.popup(cursor.pos())
      self.popMenu.exec_()
