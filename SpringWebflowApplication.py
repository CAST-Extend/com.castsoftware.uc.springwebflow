'''
Created on 2 feb 2017

@author: TGU
'''
import cast_upgrades.cast_upgrade_1_5_16 # @UnusedImport

import xml.etree.ElementTree as ET
from cast.application import ApplicationLevelExtension, create_link
import logging

class TilesAndSpringWebflowApplication(ApplicationLevelExtension):

    def __init__(self):      
        self.jsp = {} 
        self.jsp_webapp = {}         
        self.beans = {}
        self.javaClasses= {}
        self.javaClassesFullName = {}
        self.javaClasses_webapp= {}
        self.javaMethods = {}
        self.javaEnumItems = {}        
        self.tilesDefs = {}
        self.tilesDefTemplates = {}
        self.tilesDefExtends = {}
        self.viewStates = {}
        self.decisionStates = {}
        self.actionStates = {}        
        self.onstart = {}  
        
        self.target_links = {} 
        
    def end_application(self, application):
        self.global_nb_links = 0 
                
        # tests lines 
        #file_full_name = "C:\\CASTMSdvptextensions\\Deploy\\CPP2017\\mapi\\mapi\\mapi\\administration\\src\\main\\webapp\\WEB-INF\\tiles\\structure\\modifier\\tiles-modifier.xml" 
        #file_full_name = "C:\\CASTMSAIFECPP2017\\Deploy\\CPP2017\\My Package\\mapi\\administration\\src\\main\\webapp\\WEB-INF\\tiles\\utilisateur\\tiles-utilisateur.xml"
        #file_full_name = "C:\\CASTMSdvptextensions\\Deploy\\CPP2017\\mapi\\mapi\\mapi\\administration\\src\\main\\webapp\\WEB-INF\\flows\\structure\\modifier\\modifier-flux.xml" 
        #self.display_XMLTiles_files(application, file_full_name)
        #self.display_XMLSpringWebflow_files(application, file_full_name)   
        # end tests lines  
        
        #self.links_from_Tiles_to_JSP(application)
        #self.links_from_JSP_to_Tiles(application)
        
        
        self.JSP_List(application) 
        self.JSP_webapp_List(application)       
        self.BeansList(application)
        self.JavaClassList(application)
        self.JavaClassFullNameList(application)
        self.JavaMethodList(application)
        self.JavaEnumItemList(application)        
        self.ApacheTilesDefinitionList(application)
        self.ApacheTilesDefinitionTemplateList(application)
        self.ApacheTilesDefinitionExtendsList(application)
        self.ViewStateList(application)
        self.handle_ViewStates(application)
        self.handle_DecisionState(application)
        self.handle_ActionState(application)
        self.handle_SubFlowState(application)
        self.handle_OnStart(application)        
        
        
        #self.JSP_webapp_List(application)       
        
        logging.info("Nb of links created globally : " + str(self.global_nb_links)) 


    def JSP_List(self, application): 
           
        for o in application.get_files(['CAST_Web_File']): 
            
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if (not o.get_path().lower().endswith('.jsp')) and (not o.get_path().lower().endswith('.jspx')) and (not o.get_path().lower().endswith('.xhtml')): # check if JSP file
                continue
            
            #logging.info("o getPath = [" + o.get_path() + "]") 
            
            if 'webapp' in o.get_path():        # check webapp in JSP name 
                jsp_name = str(o.get_fullname()).split('webapp')[1].replace(']', '').replace('\\', '/')
                logging.info("jsp_name1 = [" + jsp_name + "]") 
                self.jsp[jsp_name] = o   
            elif 'meta-inf' in o.get_path():
                jsp_name = str(o.get_fullname()).split('META-INF\\resources')[1].replace(']', '').replace('\\', '/')
                logging.info("jsp_name2 = [" + jsp_name + "]") 
                self.jsp[jsp_name] = o 
            else: 
                logging.info("jsp_name without webapp 1 = " + str(o.get_fullname()))
                continue 
            
    def JSP_webapp_List(self, application): 
           
        for o in application.get_files(['CAST_Web_File']): 
            
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            
            if (not o.get_path().lower().endswith('.jsp')) and (not o.get_path().lower().endswith('.jspx')) and (not o.get_path().lower().endswith('.xhtml')): # check if JSP file
                continue
            
            if not ('webapp') in o.get_path():            # check webapp in JSP name 
                logging.info("jsp_name without webapp 2= " + str(o.get_fullname()))
                continue
            
            jsp_name = str(o.get_fullname()).split('webapp')[1].replace(']', '').replace('\\', '/')
            logging.info("jsp_name = [" + jsp_name + "]") 
            
            webapp = self.webapp_container(o)
            logging.info("jsp webapp = [" + webapp + "]") 
            
            webapp_jsp_name = webapp + '#' + jsp_name 
            
            self.jsp_webapp[webapp_jsp_name] = o       
    
    def JavaClassList(self, application):

        for javaClass in application.objects().has_type('Java').has_type('JV_CLASS'):     
            javaClass_name = javaClass.get_name()
            #javaClass_fullname = javaClass.get_fullname()
            logging.info("Java Class Name = [" + javaClass_name + "]") 
            #logging.info("Java Class full Name = " + javaClass_fullname) 
            self.javaClasses[javaClass_name] = javaClass                 

    def JavaClassFullNameList(self, application):

        for javaClass in application.objects().has_type('Java').has_type('JV_CLASS'):     
            javaClass_name = javaClass.get_name()
            javaClass_fullname = javaClass.get_fullname()
            #logging.info("Java Class Name = [" + javaClass_name + "]") 
            logging.info("Java Class full Name [" + str(javaClass_name) + "]= " + javaClass_fullname) 
            self.javaClassesFullName[javaClass_name] = javaClass_fullname      
    
    def JavaMethodList(self, application):

        for javaMethod in application.objects().has_type('Java').has_type('JV_METHOD'):     
            #javaMethod_name = javaMethod.get_name()
            javaMethod_fullname = javaMethod.get_fullname()
            #logging.info("Java Method Name = " + javaMethod_name) 
            #logging.info("Java Method full Name = " + javaMethod_fullname) 
            self.javaMethods[javaMethod_fullname] = javaMethod
       
       
    def JavaEnumItemList(self, application):

        for javaEnumItem in application.objects().has_type('Java').has_type('JV_ENUM_ITEM'):     
            #javaEnumItem_name = javaEnumItem.get_name()
            javaEnumItem_fullname = javaEnumItem.get_fullname()
            #logging.info("Java Enum Item Name = " + javaEnumItem_name) 
            #logging.info("Java Enum Item full Name = " + javaEnumItem_fullname) 
            self.javaEnumItems[javaEnumItem_fullname] = javaEnumItem       
       
    def BeansList(self, application):

        # all classes with a link to a Spring Bean 
        for link in application.links().has_callee(application.objects().is_class()).has_caller(application.objects().has_type('SPRING_BEAN')):
            bean_name = link.get_caller().get_name()
            class_fullname = link.get_callee().get_fullname()
            logging.debug("Spring Bean [" + bean_name + "] ==== linked to class [" + class_fullname + "]")
            self.beans[bean_name] = class_fullname
            
    def ApacheTilesDefinitionList(self, application):
    
        for tilesDef in application.objects().has_type('TilesDefinition'):     
            tilesDef_name = tilesDef.get_name()
            logging.info("tilesDefinition Name = [" + tilesDef_name + "]") 
            self.tilesDefs[tilesDef_name] = tilesDef
            
            
    def ApacheTilesDefinitionTemplateList(self, application):
    
        for tilesDef in application.objects().has_type('TilesDefinition').load_property('TilesDefinition.definition_template'):     
            tilesDef_name = tilesDef.get_name()
            logging.info("tilesDefinition Name = [" + tilesDef_name + "]") 
            tilesDef_template = tilesDef.get_property('TilesDefinition.definition_template')
            logging.info("tilesDefinition Template = [" + tilesDef_name + "]") 
            self.tilesDefTemplates[tilesDef_name] = tilesDef_template   
            
    def ApacheTilesDefinitionExtendsList(self, application):
    
        for tilesDef in application.objects().has_type('TilesDefinition').load_property('TilesDefinition.definition_extends'):     
            tilesDef_name = tilesDef.get_name()
            logging.info("tilesDefinition Name = [" + tilesDef_name + "]") 
            tilesDef_extends = tilesDef.get_property('TilesDefinition.definition_extends')
            logging.info("tilesDefinition Extends = [" + tilesDef_name + "]") 
            self.tilesDefExtends[tilesDef_name] = tilesDef_extends                        
    
    def ViewStateList(self, application):
            
        for viewState in application.objects().has_type('SpringWebFlowViewState').load_property('SpringWebFlowViewState.view_state_view').load_property('SpringWebFlowViewState.view_state_model'):     
            logging.info("Web Flow Id = " + viewState.get_name()) 
            view_state_view = viewState.get_property('SpringWebFlowViewState.view_state_view')
            logging.info("== view_state_view = [" + str(view_state_view) + "]")             
            view_state_model = viewState.get_property('SpringWebFlowViewState.view_state_model')
            logging.info("== view_state_model = [" + str(view_state_model) + "]")             
            self.viewStates[viewState.get_fullname()] = viewState             
       
    def handle_ViewStates(self, application):
        
        nb_links = 0 
        nb_links2 = 0 
        nb_notfound = 0
        nb_notfound2 = 0 
                
        for view_state in application.objects().has_type('SpringWebFlowViewState').load_property('SpringWebFlowViewState.view_state_view').load_property('SpringWebFlowViewState.view_state_on_entry_evaluate').load_property('SpringWebFlowViewState.view_state_on_render_evaluate').load_property('SpringWebFlowViewState.view_state_on_exit_evaluate').load_property('SpringWebFlowViewState.transition_evaluate'):     
            view_states_fullname = view_state.get_fullname()
            logging.info(" View-state_fullname : [" + str(view_states_fullname) + "]")
            view_states = self.viewStates[view_states_fullname]
            view_states_name = view_states.get_name()
            logging.info(" View-state name : [" + str(view_states_name) + "]")
            logging.info(" View-state : [" + str(self.viewStates[view_states_fullname]) + "]")
            
            JSP_view = None
            
            if view_states_name in self.tilesDefs: 
                tilesDef = self.tilesDefs[view_states_name]
                logging.info(" Tiles Def Name :: [" + str(tilesDef) + "]")

                tilesDefTemplate = self.tilesDefTemplates[str(tilesDef.get_name())]
                    
                if '.jsp' in str(tilesDefTemplate) and str(tilesDefTemplate) in self.jsp: 
                    JSP_view = self.jsp[str(tilesDefTemplate)] 
                    logging.info(" JSP View Template : [" + str(tilesDefTemplate) + "]")
                
                if str(tilesDef.get_name()) in self.tilesDefExtends: 
                    tilesDefExtends = self.tilesDefExtends[str(tilesDef.get_name())]
                    logging.info(" Extends Name : [" + str(tilesDefExtends) + "]")
                
                if tilesDefTemplate is None: 
                    logging.info(" Search for Extends")
                    if tilesDefExtends in self.tilesDefTemplates: 
                        tilesDefTemplateTarget = str(self.tilesDefTemplates[tilesDefExtends]) 
                        logging.info(" Tiles Def Template Target : [" + tilesDefTemplateTarget + "]")
                        logging.info(" Search for JSP View")
                        
                        webapp = self.webapp_container(view_state)
                        logging.info(" tilesDef webapp : [" + str(webapp) + "]")
                        web_app_jsp = webapp + '#' + tilesDefTemplateTarget
                        #if (web_app_jsp) in self.jsp_webapp: 
                        if tilesDefTemplateTarget in self.jsp: 
                            JSP_view = self.jsp[tilesDefTemplateTarget]  
                            logging.info(" JSP View : [" + str(JSP_view.get_fullname()) + "]")
                        else: 
                            logging.info(" JSP View not found : [" + tilesDefTemplateTarget + "] in webapp [" + webapp + "]")
                            nb_notfound += 1 
            else:                                           # no TilesDefs (no Apache Tiles definition, directly JSP)
                JSP_identification = view_state.get_property('SpringWebFlowViewState.view_state_view')
                logging.info(" JSP View identification : [" + str(JSP_identification) + "]")
                if JSP_identification in self.jsp: 
                    JSP_view = self.jsp[str(JSP_identification)]
                    logging.info(" JSP View 1 : [" + str(JSP_view.get_fullname()) + "]")
                else: 
                    logging.info(" JSP not found 1 : [" + str(JSP_identification) + "]")
                        
            # define a link for the transition evaluate 
            view_state_evaluate = view_state.get_property('SpringWebFlowViewState.view_state_on_entry_evaluate')
  
            if not view_state_evaluate is None: 
                logging.info("== view_state_on_entry_evaluate global = [" + str(view_state_evaluate) + "]") 
                for evaluate in (str(view_state_evaluate)).split("#"): 

                    view_state_evaluate_bean_name = ""
                    view_state_evaluate_method_name = ""
                    view_state_evaluate_method_full_name = ""   
                    
                    if not evaluate == "": 
                        logging.info("== view_state_on_entry_evaluate = [" + str(evaluate) + "]") 
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                            
                                view_state_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                view_state_evaluate_bean_full_name = ""
                                if view_state_evaluate_bean_name in self.beans: 
                                    view_state_evaluate_bean_full_name = self.beans[view_state_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    view_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    view_state_evaluate_method_full_name = view_state_evaluate_bean_full_name + '.' + view_state_evaluate_method_name
                                    logging.info("== view_state_on_entry_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                else: 
                                    logging.info("bean not found 1: [" + view_state_evaluate_bean_name + "] now looking for class")
                                    view_state_evaluate_class_name = view_state_evaluate_bean_name 
                                    view_state_evaluate_class_name_upper = view_state_evaluate_class_name[0].upper() + view_state_evaluate_class_name[1:] 
                                    logging.info("class searched 1 = [" + view_state_evaluate_class_name +"] & class searched 2 = [" + view_state_evaluate_class_name_upper +"]") 
                                    if (view_state_evaluate_class_name in self.javaClasses) or (view_state_evaluate_class_name_upper in self.javaClassesFullName): 
                                        if view_state_evaluate_class_name_upper in self.javaClassesFullName:
                                            view_state_evaluate_class_full_name = self.javaClassesFullName[view_state_evaluate_class_name_upper]
                                        else: 
                                            view_state_evaluate_class_full_name = self.javaClasses[view_state_evaluate_class_name]
                                        #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                        view_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                        #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                        view_state_evaluate_method_full_name =view_state_evaluate_class_full_name + '.' +view_state_evaluate_method_name
                                        logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                       
                                    else: 
                                        logging.info("class also not found : [" + view_state_evaluate_class_name + "]")
                                        nb_notfound2 += 1                                    
                                    
                            else: # class full name  
                                view_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + view_state_evaluate_class_full_name + "]") 
                                view_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                view_state_evaluate_method_full_name = view_state_evaluate_class_full_name + '.' + view_state_evaluate_method_name
                                logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                
                            if not view_state_evaluate_method_full_name == "": 
                                if view_state_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[view_state_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the JSP and the method 
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java method target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                    else: 
                                        logging.info("JSP_view is None 1")

                                    # create the link between the view-state object and the method 
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1    
                                    
                                    
                                elif view_state_evaluate_method_full_name in self.javaEnumItems: 
                                    java_method_target = self.javaEnumItems[view_state_evaluate_method_full_name]
                                    logging.info("== java Enum Item target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the JSP and the enum item  
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java Enum Item target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                    else: 
                                        logging.info("JSP_view is None 2")
                                        
                                    # create the link between the view-state object and the enum item  
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1                                        
                                    
                                    
                                else: 
                                    logging.info("== java method or Enum Item target not found = [" + str(view_state_evaluate_method_full_name) + "]")
                                    nb_notfound2 += 1 

                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound2 += 1 

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== evaluate_on_entry global is null") 


            # define a link for the transition evaluate 
            view_state_evaluate = view_state.get_property('SpringWebFlowViewState.view_state_on_render_evaluate')
            if not view_state_evaluate is None: 
                logging.info("== view_state_on_entry_evaluate global = [" + str(view_state_evaluate) + "]") 
                for evaluate in (str(view_state_evaluate)).split("#"): 
                    logging.info("== view_state_on_entry_evaluate = [" + str(evaluate) + "]") 
                    view_state_evaluate_bean_name = ""
                    view_state_evaluate_method_name = ""
                    view_state_evaluate_method_full_name = ""
                    
                    if not evaluate == "": 
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                            
                                view_state_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                view_state_evaluate_bean_full_name = ""
                                if view_state_evaluate_bean_name in self.beans: 
                                    view_state_evaluate_bean_full_name = self.beans[view_state_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    view_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    view_state_evaluate_method_full_name = view_state_evaluate_bean_full_name + '.' + view_state_evaluate_method_name
                                    logging.info("== view_state_on_entry_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                else: 
                                    logging.info("bean not found 2: [" + view_state_evaluate_bean_name + "] now looking for class")
                                
                                    view_state_evaluate_class_name = view_state_evaluate_bean_name 
                                    view_state_evaluate_class_name_upper = view_state_evaluate_class_name[0].upper() + view_state_evaluate_class_name[1:] 
                                    logging.info("class searched 1 = [" + view_state_evaluate_class_name + "] & class searched 2 = [" + view_state_evaluate_class_name_upper +"]") 
                                    if (view_state_evaluate_class_name in self.javaClasses) or (view_state_evaluate_class_name_upper in self.javaClassesFullName): 
                                        if view_state_evaluate_class_name_upper in self.javaClassesFullName:
                                            view_state_evaluate_class_full_name = self.javaClassesFullName[view_state_evaluate_class_name_upper]
                                        else: 
                                            view_state_evaluate_class_full_name = self.javaClasses[view_state_evaluate_class_name]
                                        #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                        view_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                        #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                        view_state_evaluate_method_full_name = view_state_evaluate_class_full_name + '.' + view_state_evaluate_method_name
                                        logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                       
                                    else: 
                                        logging.info("class also not found : [" + view_state_evaluate_class_name + "]")
                                        nb_notfound2 += 1 
                                    
                            else: # class full name  
                                view_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + view_state_evaluate_class_full_name + "]") 
                                view_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                view_state_evaluate_method_full_name = view_state_evaluate_class_full_name + '.' + view_state_evaluate_method_name
                                logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                
                            if not view_state_evaluate_method_full_name == "": 
                                if view_state_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[view_state_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the JSP and the method 
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java method target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                    else: 
                                        logging.info("JSP_view is None 3")
                                        
                                    # create the link between the view-state object and the method 
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1    

                                elif view_state_evaluate_method_full_name in self.javaEnumItems: 
                                    java_method_target = self.javaEnumItems[view_state_evaluate_method_full_name]
                                    logging.info("== java Enum Item target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the JSP and the enum item  
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java Enum Item target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                    else: 
                                        logging.info("JSP_view is None 4")
                                        
                                    # create the link between the view-state object and the enum item  
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1    
  
                                else: 
                                    logging.info("== java Method or Enum Item target not found = [" + str(view_state_evaluate_method_full_name) + "]")
                                    nb_notfound2 += 1 

                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound2 += 1 

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== evaluate_on_render global is null") 


            # define a link for the transition evaluate 
            view_state_evaluate = view_state.get_property('SpringWebFlowViewState.view_state_on_exit_evaluate')
            if not view_state_evaluate is None: 
                logging.info("== view_state_on_exit_evaluate global = [" + str(view_state_evaluate) + "]") 
                for evaluate in (str(view_state_evaluate)).split("#"): 
                    logging.info("== view_state_on_exit_evaluate = [" + str(evaluate) + "]") 
                    view_state_evaluate_bean_name = ""
                    view_state_evaluate_method_name = ""
                    view_state_evaluate_method_full_name = ""
                    
                    if not evaluate == "": 
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                            
                                view_state_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                view_state_evaluate_bean_full_name = ""
                                if view_state_evaluate_bean_name in self.beans: 
                                    view_state_evaluate_bean_full_name = self.beans[view_state_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    view_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    view_state_evaluate_method_full_name = view_state_evaluate_bean_full_name + '.' + view_state_evaluate_method_name
                                    logging.info("== view_state_on_exit_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                else: 
                                    logging.info("bean not found 3: [" + view_state_evaluate_bean_name + "]")
                                    nb_notfound2 += 1 
                                    
                            else: # class full name  
                                view_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + view_state_evaluate_class_full_name + "]") 
                                view_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                view_state_evaluate_method_full_name = view_state_evaluate_class_full_name + '.' + view_state_evaluate_method_name
                                logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                
                            if not view_state_evaluate_method_full_name == "": 
                                if view_state_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[view_state_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the JSP and the method 
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java method target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                        
                                    else: 
                                        logging.info("JSP_view is None 5")
                                        
                                    # create the link between the view-state object and the method 
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1    

                                elif view_state_evaluate_method_full_name in self.javaEnumItems: 
                                    java_method_target = self.javaEnumItems[view_state_evaluate_method_full_name]
                                    logging.info("== java Enum Item target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the JSP and the enum item  
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java Enum Item target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                        
                                    else: 
                                        logging.info("JSP_view is None 6")
                                        
                                    # create the link between the view-state object and the enum item  
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1    
  
                                else: 
                                    logging.info("== java Method or Enum Item target not found = [" + str(view_state_evaluate_method_full_name) + "]")
                                    nb_notfound2 += 1 

                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound2 += 1 

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== evaluate_on_exit global is null") 
                


            # define a link for the transition evaluate 
            transition_evaluate = view_state.get_property('SpringWebFlowViewState.transition_evaluate')
            if not transition_evaluate is None: 
                logging.info("== transition_evaluate global = [" + str(transition_evaluate) + "]") 
                for evaluate in (str(transition_evaluate)).split("#"): 
                    
                    transition_evaluate_bean_name = ""
                    transition_evaluate_bean_full_name = ""                         
                    transition_evaluate_method_name = ""
                    transition_evaluate_method_full_name = ""        
                    
                    if not evaluate == "": 
                        logging.info("== transition_evaluate = [" + str(evaluate) + "]") 
                        if '.' in evaluate: 
                        
                            if evaluate.count('.') == 1: # bean 
                                transition_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                transition_evaluate_bean_full_name = ""
                                if transition_evaluate_bean_name in self.beans: 
                                    transition_evaluate_bean_full_name = self.beans[transition_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                else:
                                    logging.info("bean not found 4: [" + transition_evaluate_bean_name + "] now looking for class")
                                    transition_evaluate_class_name = transition_evaluate_bean_name 
                                    transition_evaluate_class_name_upper = transition_evaluate_class_name[0].upper() + transition_evaluate_class_name[1:] 
                                    logging.info("class searched 1 = [" + transition_evaluate_class_name +"] & class searched 2 = [" + transition_evaluate_class_name_upper +"]") 
                                    if (transition_evaluate_class_name in self.javaClasses) or (transition_evaluate_class_name_upper in self.javaClassesFullName): 
                                        if transition_evaluate_class_name_upper in self.javaClassesFullName:
                                            transition_evaluate_class_full_name = self.javaClassesFullName[transition_evaluate_class_name_upper]
                                        else: 
                                            transition_evaluate_class_full_name = self.javaClasses[transition_evaluate_class_name]
                                        #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                        transition_evaluate_method_name = (str(evaluate)).split('.')[1]
                                        #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                        transition_evaluate_method_full_name = transition_evaluate_class_full_name + '.' + transition_evaluate_method_name
                                        logging.info("== transition_evaluate method full name = [" + transition_evaluate_method_full_name + "]")                                       
                                    else: 
                                        logging.info("class also not found : [" + transition_evaluate_class_name + "]")
                                        nb_notfound += 1                                        
                                        
                                        
                            else: # class full name  
                                view_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + view_state_evaluate_class_full_name + "]") 
                                view_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                view_state_evaluate_method_full_name = view_state_evaluate_class_full_name + '.' + view_state_evaluate_method_name
                                logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                                                
                                                                
                            if not transition_evaluate_method_full_name == "": 
                                if transition_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[transition_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the view and the method 
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java method target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                    else: 
                                        logging.info("JSP_view is None 7")
        
                                    # create the link between the transition object and the method 
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1 
                                        
                                elif transition_evaluate_method_full_name in self.javaEnumItems: 
                                    java_method_target = self.javaEnumItems[view_state_evaluate_method_full_name]
                                    logging.info("== java Enum Item target = [" + str(java_method_target) + "]")
                                    if not JSP_view is None: 
                                        # create the link between the JSP and the enum item  
                                        create_link('callLink', JSP_view, java_method_target)
                                        logging.info("== link created between JSP + [" + str(JSP_view.get_fullname()) + "] and java Enum Item target = [" + str(java_method_target) + "]")
                                        nb_links += 1 
                                    else: 
                                        logging.info("JSP_view is None 8")
                                        
                                    # create the link between the view-state object and the enum item  
                                    create_link('callLink', view_state, java_method_target)
                                    nb_links2 += 1                                            
                                         
                                else: 
                                    logging.info("== java Method or Enum Item target not found = [" + str(transition_evaluate_method_full_name) + "]")
                                    nb_notfound2 += 1
                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound2 += 1

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== transition_evaluate global is null") 


        logging.debug(">>>>>> Nb of links created between JSP and method determined through View-state evaluate : " + str(nb_links))       
        logging.debug(">>>>>> Nb of links not created between JSP and method determined through View-state evaluate : " + str(nb_notfound))      
        logging.debug(">>>>>> Nb of links created between View-state object and method determined through View-State evaluate : " + str(nb_links2))
        logging.debug(">>>>>> Nb of links not created between View-state object and method determined through View-State evaluate : " + str(nb_notfound2))
        self.global_nb_links += nb_links 
        self.global_nb_links += nb_links2   


    def handle_DecisionState(self, application):
        
        nb_links = 0 
        nb_notfound = 0 
                
        for decision_state in application.objects().has_type('SpringWebFlowDecisionState').load_property('SpringWebFlowDecisionState.decision_state_evaluate').load_property('SpringWebFlowDecisionState.decision_state_on_entry_evaluate').load_property('SpringWebFlowDecisionState.decision_state_on_exit_evaluate'):     
            decision_state_fullname = decision_state.get_fullname()
            logging.info(" Decision-state_fullname : [" + str(decision_state_fullname) + "]")
            
            decision_state_evaluate_bean_name = ""
            decision_state_evaluate_method_name = ""
            decision_state_evaluate_bean_full_name = "" 
            decision_state_evaluate_method_full_name = ""
            
            # define a link for the transition evaluate 
            decision_state_evaluate = decision_state.get_property('SpringWebFlowDecisionState.decision_state_evaluate')
            if not decision_state_evaluate is None: 
                logging.info("== decision_state_evaluate global = [" + str(decision_state_evaluate) + "]") 
                for evaluate in (str(decision_state_evaluate)).split("#"): 
                    if not evaluate == "": 
                        logging.info("== decision_state_evaluate = [" + str(evaluate) + "]") 
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                            
                                decision_state_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                decision_state_evaluate_bean_full_name = ""
                                try: 
                                    decision_state_evaluate_bean_full_name = self.beans[decision_state_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    decision_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    decision_state_evaluate_method_full_name = decision_state_evaluate_bean_full_name + '.' + decision_state_evaluate_method_name
                                    logging.info("== decision_state_evaluate method full name = [" + decision_state_evaluate_method_full_name + "]")                                
                                
                                except KeyError: 
                                    logging.info("bean not found 5: [" + decision_state_evaluate_bean_name + "]")
                                    nb_notfound += 1
                                    
                            else: # class full name  
                                decision_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== decision_evaluate class full name = [" + decision_state_evaluate_class_full_name + "]") 
                                decision_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                decision_state_evaluate_method_full_name = decision_state_evaluate_class_full_name + '.' + decision_state_evaluate_method_name
                                logging.info("== decision_state_evaluate method full name = [" + decision_state_evaluate_method_full_name + "]")                                
                                
                            if not decision_state_evaluate_method_full_name == "": 
                                if decision_state_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[decision_state_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
    
                                    # create the link between the decision-state object and the method 
                                    create_link('callLink', decision_state, java_method_target)
                                    nb_links += 1    
                                        
                                else: 
                                    logging.info("== java method target not found = [" + str(decision_state_evaluate_method_full_name) + "]")
                                    nb_notfound += 1    

                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound += 1 
                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== decision_evaluate global is null") 
           
           
           
            # define a link for the transition evaluate 
            decision_state_evaluate = decision_state.get_property('SpringWebFlowDecisionState.decision_state_on_entry_evaluate')
            if not decision_state_evaluate is None: 
                logging.info("== decision_state_on_entry_evaluate global = [" + str(decision_state_evaluate) + "]") 
                for evaluate in (str(decision_state_evaluate)).split("#"): 
                    logging.info("== decision_state_on_entry_evaluate = [" + str(evaluate) + "]") 
                    decision_state_evaluate_bean_name = ""
                    decision_state_evaluate_method_name = ""
                    decision_state_evaluate_method_full_name = ""
                    
                    if not evaluate == "": 
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                            
                                decision_state_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                decision_state_evaluate_bean_full_name = ""
                                if decision_state_evaluate_bean_name in self.beans: 
                                    decision_state_evaluate_bean_full_name = self.beans[decision_state_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    decision_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    decision_state_evaluate_method_full_name = decision_state_evaluate_bean_full_name + '.' + decision_state_evaluate_method_name
                                    logging.info("== decision_state_on_entry_evaluate method full name = [" + decision_state_evaluate_method_full_name + "]")                                
                                else: 
                                    logging.info("bean not found 6: [" + decision_state_evaluate_bean_name + "]")
                                    nb_notfound += 1 
                                    
                            else: # class full name  
                                decision_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + decision_state_evaluate_class_full_name + "]") 
                                decision_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                decision_state_evaluate_method_full_name = decision_state_evaluate_class_full_name + '.' + decision_state_evaluate_method_name
                                logging.info("== decision_state_on_entry_evaluate method full name = [" + decision_state_evaluate_method_full_name + "]")                                
                                
                            if not decision_state_evaluate_method_full_name == "": 
                                if decision_state_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[decision_state_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")   
                                    # create the link between the decision-state object and the method 
                                    create_link('callLink', decision_state, java_method_target)
                                    nb_links += 1    

                                elif decision_state_evaluate_method_full_name in self.javaEnumItems: 
                                    java_method_target = self.javaEnumItems[decision_state_evaluate_method_full_name]
                                    logging.info("== java Enum Item target = [" + str(java_method_target) + "]")
                                    # create the link between the decision-state object and the enum item  
                                    create_link('callLink', decision_state, java_method_target)
                                    nb_links += 1    
  
                                else: 
                                    logging.info("== java Method or Enum Item target not found = [" + str(decision_state_evaluate_method_full_name) + "]")
                                    nb_notfound += 1 

                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound += 1 

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== evaluate_on_entry global is null")            
           

            # define a link for the transition evaluate 
            decision_state_evaluate = decision_state.get_property('SpringWebFlowDecisionState.decision_state_on_exit_evaluate')
            if not decision_state_evaluate is None: 
                logging.info("== decision_state_on_exit_evaluate global = [" + str(decision_state_evaluate) + "]") 
                for evaluate in (str(decision_state_evaluate)).split("#"): 
                    logging.info("== decision_state_on_exit_evaluate = [" + str(evaluate) + "]") 
                    decision_state_evaluate_bean_name = ""
                    decision_state_evaluate_method_name = ""
                    decision_state_evaluate_method_full_name = ""
                    
                    if not evaluate == "": 
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                            
                                decision_state_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                decision_state_evaluate_bean_full_name = ""
                                if decision_state_evaluate_bean_name in self.beans: 
                                    decision_state_evaluate_bean_full_name = self.beans[decision_state_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    decision_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    decision_state_evaluate_method_full_name = decision_state_evaluate_bean_full_name + '.' + decision_state_evaluate_method_name
                                    logging.info("== decision_state_on_exit_evaluate method full name = [" + decision_state_evaluate_method_full_name + "]")                                
                                else: 
                                    logging.info("bean not found 7: [" + decision_state_evaluate_bean_name + "]")
                                    nb_notfound += 1 
                                    
                            else: # class full name  
                                decision_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + decision_state_evaluate_class_full_name + "]") 
                                decision_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                decision_state_evaluate_method_full_name = decision_state_evaluate_class_full_name + '.' + decision_state_evaluate_method_name
                                logging.info("== decision_state_on_exit_evaluate method full name = [" + decision_state_evaluate_method_full_name + "]")                                
                                
                            if not decision_state_evaluate_method_full_name == "": 
                                if decision_state_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[decision_state_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")   
                                    # create the link between the decision-state object and the method 
                                    create_link('callLink', decision_state, java_method_target)
                                    nb_links += 1    

                                elif decision_state_evaluate_method_full_name in self.javaEnumItems: 
                                    java_method_target = self.javaEnumItems[decision_state_evaluate_method_full_name]
                                    logging.info("== java Enum Item target = [" + str(java_method_target) + "]")
                                    # create the link between the decision-state object and the enum item  
                                    create_link('callLink', decision_state, java_method_target)
                                    nb_links += 1    
  
                                else: 
                                    logging.info("== java Method or Enum Item target not found = [" + str(decision_state_evaluate_method_full_name) + "]")
                                    nb_notfound += 1 

                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound += 1 

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== evaluate_on_exit global is null")            
           
                
        logging.debug(">>>>>> Nb of links created between Decision-state object and method determined through Decision-State evaluate : " + str(nb_links))
        logging.debug(">>>>>> Nb of links not created between Decision-state object and method determined through Decision-State evaluate : " + str(nb_notfound))
        self.global_nb_links += nb_links              
               

    def handle_ActionState(self, application):
        
        nb_links = 0
        nb_notfound = 0  
                
        for action_state in application.objects().has_type('SpringWebFlowActionState').load_property('SpringWebFlowActionState.action_state_evaluate').load_property(('SpringWebFlowViewState.transition_evaluate')):     
            action_states_fullname = action_state.get_fullname()
            logging.info(" Action-state_fullname : [" + str(action_states_fullname) + "]")
            
            # define a link for the transition evaluate 
            action_state_evaluate = action_state.get_property('SpringWebFlowActionState.action_state_evaluate')
            if not action_state_evaluate is None: 
                logging.info("== action_state_evaluate global = [" + str(action_state_evaluate) + "]") 
                for evaluate in (str(action_state_evaluate)).split("#"): 
                    if not evaluate == "": 
                        logging.info("== action_state_evaluate = [" + str(evaluate) + "]") 
                        action_state_evaluate_method_full_name = "" 
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                            
                                action_state_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                action_state_evaluate_bean_full_name = ""
                                try: 
                                    action_state_evaluate_bean_full_name = self.beans[action_state_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    action_state_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    action_state_evaluate_method_full_name = action_state_evaluate_bean_full_name + '.' + action_state_evaluate_method_name
                                    logging.info("== action_state_evaluate method full name = [" + action_state_evaluate_method_full_name + "]")                                
                                
                                except KeyError: 
                                    logging.info("bean not found 8: [" + action_state_evaluate_bean_name + "]")
                                    nb_notfound += 1
                                    
                            else: # class full name  
                                action_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== action_evaluate class full name = [" + action_state_evaluate_class_full_name + "]") 
                                action_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== action_evaluate method name = [" + transition_evaluate_method_name + "]")
                                action_state_evaluate_method_full_name = action_state_evaluate_class_full_name + '.' + action_state_evaluate_method_name
                                logging.info("== action_state_evaluate method full name = [" + action_state_evaluate_method_full_name + "]")                                
                                
                            if not action_state_evaluate_method_full_name == "": 
                                if action_state_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[action_state_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
    
                                    # create the link between the action-state object and the method 
                                    create_link('callLink', action_state, java_method_target)
                                    nb_links += 1    
                                        
                                else: 
                                    logging.info("== java method target not found = [" + str(action_state_evaluate_method_full_name) + "]")
                                    nb_notfound += 1    

                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound += 1 
                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== Action_evaluate global is null") 
                
                
            # define a link for the transition evaluate 
            transition_evaluate = action_state.get_property('SpringWebFlowViewState.transition_evaluate')
            if not transition_evaluate is None: 
                logging.info("== transition_evaluate global = [" + str(transition_evaluate) + "]")                 
                for evaluate in (str(transition_evaluate)).split("#"): 
                    if not evaluate == "": 
                        logging.info("== transition_evaluate = [" + str(evaluate) + "]") 
                        if '.' in evaluate: 
                            transition_evaluate_method_full_name = ""
                        
                            if evaluate.count('.') == 1: # bean 
                                transition_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                transition_evaluate_bean_full_name = ""
                                try: 
                                    transition_evaluate_bean_full_name = self.beans[transition_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                except KeyError: 
                                        logging.info("bean not found 10: [" + transition_evaluate_bean_name + "]")
                                        
                                transition_evaluate_method_name = (str(evaluate)).split('.')[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                transition_evaluate_method_full_name = transition_evaluate_bean_full_name + '.' + transition_evaluate_method_name
                                logging.info("== transition_evaluate method full name = [" + transition_evaluate_method_full_name + "]")
                                
                            else: # class full name  
                                view_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + view_state_evaluate_class_full_name + "]") 
                                view_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                view_state_evaluate_method_full_name = view_state_evaluate_class_full_name + '.' + view_state_evaluate_method_name
                                logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                                                
                                                                
                            if not transition_evaluate_method_full_name == "": 
                                if transition_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[transition_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
        
                                    # create the link between the transition object and the method 
                                    create_link('callLink', action_state, java_method_target)
                                    nb_links += 1 
                                            
                                else: 
                                    logging.info("== java method target not found = [" + str(transition_evaluate_method_full_name) + "]")
                                    nb_notfound += 1
                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound += 1

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== transition_evaluate global is null")                 
                
                               
        logging.debug(">>>>>> Nb of links created between Action-state object and method determined through Action-State evaluate : " + str(nb_links))
        logging.debug(">>>>>> Nb of links not created between Action-state object and method determined through Action-State evaluate : " + str(nb_notfound))
        self.global_nb_links += nb_links                  

    def handle_SubFlowState(self, application):
        
        nb_links = 0
        nb_notfound = 0  
                
        for subFlow_state in application.objects().has_type('SpringWebFlowSubFlow').load_property('SpringWebFlowSubFlow.transition_evaluate'):     
            subFlow_states_fullname = subFlow_state.get_fullname()
            logging.info(" SubFlow-state_fullname : [" + str(subFlow_states_fullname) + "]")
                           
                
            # define a link for the transition evaluate 
            transition_evaluate = subFlow_state.get_property('SpringWebFlowSubFlow.transition_evaluate')
            if not transition_evaluate is None: 
                logging.info("== transition_evaluate global = [" + str(transition_evaluate) + "]") 
                for evaluate in (str(transition_evaluate)).split("#"): 
                    if not evaluate == "": 
                        logging.info("== transition_evaluate = [" + str(evaluate) + "]") 
                        if '.' in evaluate: 
                            transition_evaluate_method_full_name = ""
                            
                            if evaluate.count('.') == 1: # bean 
                                transition_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                transition_evaluate_bean_full_name = ""
                                try: 
                                    transition_evaluate_bean_full_name = self.beans[transition_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                except KeyError: 
                                        logging.info("bean not found 11: [" + transition_evaluate_bean_name + "]")
                                        
                                transition_evaluate_method_name = (str(evaluate)).split('.')[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                transition_evaluate_method_full_name = transition_evaluate_bean_full_name + '.' + transition_evaluate_method_name
                                logging.info("== transition_evaluate method full name = [" + transition_evaluate_method_full_name + "]")
                                
                            else: # class full name  
                                view_state_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== transition_evaluate class full name = [" + view_state_evaluate_class_full_name + "]") 
                                view_state_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                view_state_evaluate_method_full_name = view_state_evaluate_class_full_name + '.' + view_state_evaluate_method_name
                                logging.info("== view_state_evaluate method full name = [" + view_state_evaluate_method_full_name + "]")                                
                                                                
                                                                
                            if not transition_evaluate_method_full_name == "": 
                                if transition_evaluate_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[transition_evaluate_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
        
                                    # create the link between the transition object and the method 
                                    create_link('callLink', subFlow_state, java_method_target)
                                    nb_links += 1 
                                            
                                else: 
                                    logging.info("== java method target not found = [" + str(transition_evaluate_method_full_name) + "]")
                                    nb_notfound += 1
                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound += 1

                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== transition_evaluate global is null")                 
                
                               
        logging.debug(">>>>>> Nb of links created between SubFlow-state object and method determined through SubFlow-State evaluate : " + str(nb_links))
        logging.debug(">>>>>> Nb of links not created between SubFlow-state object and method determined through SubFlow-State evaluate : " + str(nb_notfound))
        self.global_nb_links += nb_links   

    def handle_OnStart(self, application):
        
        nb_links = 0 
        nb_notfound = 0 
                
        for on_start_entry in application.objects().has_type('SpringWebFlowOnStart').load_property('SpringWebFlowOnStart.on_start_evaluate'):     
            ons_start_fullname = on_start_entry.get_fullname()
            logging.info(" On-start_fullname : [" + str(ons_start_fullname) + "]")
            
            # define a link for the transition evaluate 
            on_start_evaluate = on_start_entry.get_property('SpringWebFlowOnStart.on_start_evaluate')
            if not on_start_evaluate is None: 
                logging.info("== on_start_evaluate global = [" + str(on_start_evaluate) + "]") 
                for evaluate in (str(on_start_evaluate)).split("#"): 
                    on_start_evaluate_bean_full_name = ""
                    on_start_method_full_name = ""
                    if not evaluate == "": 
                        logging.info("== on_start_evaluate = [" + str(evaluate) + "]")                         
                        if '.' in evaluate: 
                            if evaluate.count('.') == 1: # bean 
                                on_start_evaluate_bean_name = (str(evaluate)).split('.')[0]
                                #logging.info("== transition_evaluate bean name = [" + transition_evaluate_bean_name + "]") 
                                
                                if on_start_evaluate_bean_name in self.beans: 
                                    on_start_evaluate_bean_full_name = self.beans[on_start_evaluate_bean_name]
                                    #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                    on_start_evaluate_method_name = (str(evaluate)).split('.')[1]
                                    #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                    on_start_method_full_name = on_start_evaluate_bean_full_name + '.' + on_start_evaluate_method_name
                                    logging.info("== on_start_evaluate method full name = [" + on_start_method_full_name + "]")                                
                                else: 
                                    logging.info("bean not found 12: [" + on_start_evaluate_bean_name + "] now looking for class")
                                    on_start_evaluate_class_name = on_start_evaluate_bean_name 
                                    on_start_evaluate_class_name_upper = on_start_evaluate_class_name[0].upper() + on_start_evaluate_class_name[1:] 
                                    logging.info("class searched 1 = [" + on_start_evaluate_class_name +"] & class searched 2 = [" + on_start_evaluate_class_name_upper +"]") 
                                    if (on_start_evaluate_class_name in self.javaClasses) or (on_start_evaluate_class_name_upper in self.javaClassesFullName): 
                                        if on_start_evaluate_class_name_upper in self.javaClassesFullName:
                                            on_start_evaluate_class_full_name = self.javaClassesFullName[on_start_evaluate_class_name_upper]
                                        else: 
                                            on_start_evaluate_class_full_name = self.javaClasses[on_start_evaluate_class_name]
                                        #logging.info("== transition_evaluate bean full name = [" + transition_evaluate_bean_full_name + "]") 
                                        on_start_evaluate_method_name = (str(evaluate)).split('.')[1]
                                        #logging.info("== transition_evaluate method name = [" + transition_evaluate_method_name + "]")
                                        on_start_method_full_name = on_start_evaluate_class_full_name + '.' + on_start_evaluate_method_name
                                        logging.info("== on_start_evaluate method full name = [" + on_start_method_full_name + "]")                                       
                                    else: 
                                        logging.info("class also not found : [" + on_start_evaluate_class_name + "]")
                                        nb_notfound += 1
                                    
                            else: # class full name  
                                on_start_evaluate_class_full_name = (str(evaluate)).rsplit('.', 1)[0]
                                logging.info("== on_start_evaluate class full name = [" + on_start_evaluate_class_full_name + "]") 
                                on_start_evaluate_method_name = (str(evaluate)).rsplit('.', 1)[1]
                                #logging.info("== on_start_evaluate method name = [" + transition_evaluate_method_name + "]")
                                on_start_method_full_name = on_start_evaluate_class_full_name + '.' + on_start_evaluate_method_name
                                logging.info("== on_start_evaluate method full name = [" + on_start_method_full_name + "]")                                
                                
                            if not on_start_method_full_name == "": 
                                if on_start_method_full_name in self.javaMethods: 
                                    java_method_target = self.javaMethods[on_start_method_full_name]
                                    logging.info("== java method target = [" + str(java_method_target) + "]")
    
                                    # create the link between the on-start object and the method 
                                    create_link('callLink', on_start_entry, java_method_target)
                                    nb_links += 1    
                                else: 
                                    logging.info("== java method target not found = [" + str(on_start_method_full_name) + "]")
                                    nb_notfound += 1


                        else: 
                            logging.info("not able to resolve bean and method name") 
                            nb_notfound += 1
                    else: 
                        #logging.info("evaluate is null")
                        pass
            else: 
                logging.info("== On-start_evaluate global is null") 
                               
        logging.debug(">>>>>> Nb of links created between On-start object and method determined through On-Start evaluate : " + str(nb_links))
        logging.debug(">>>>>> Nb of links not created between On-start object and method determined through On-Start evaluate : " + str(nb_notfound))
        self.global_nb_links += nb_links      
        
        
                
    def links_from_Tiles_to_JSP(self, application):
        
        nb_links = 0 
        
        #for tilesDef in application.search_objects(category='TilesDefinition', load_properties=True):
        for tilesDef in application.objects().has_type('TilesDefinition').load_property('TilesDefinition.definition_template'):     

            logging.info("tilesDefinition Name = " + tilesDef.get_name()) 
            jsp_name = tilesDef.get_property('TilesDefinition.definition_template')
            logging.info("jsp target = [" + str(jsp_name) + "]") 
            try: 
                create_link('callLink', tilesDef, self.jsp[jsp_name])
                nb_links = nb_links +1 
            except KeyError: 
                logging.info("jsp not found")      
        
        logging.debug(">>>>>> Nb of links created between Tiles definition tags and JSP : " + str(nb_links))        
        self.global_nb_links += nb_links       
        nb_links = 0 
            
        #for putAtt in application.search_objects(category='TilesAttribute', load_properties=True):
        for putAtt in application.objects().has_type('TilesAttribute').load_property('TilesAttribute.put_attribute_value'):     
            # check if file is analyzed source code, or if it generated (Unknown)

            logging.info("TilesAttribute Name = " + putAtt.get_name()) 
            jsp_name = putAtt.get_property('TilesAttribute.put_attribute_value')
            logging.info("jsp target = [" + str(jsp_name) + "]") 
            try: 
                create_link('callLink', putAtt, self.jsp[jsp_name])    
                nb_links = nb_links + 1 
            except KeyError: 
                logging.info("jsp not found")         
        
        logging.debug(">>>>>> Nb of links created between Tiles put-attribute tags and JSP : " + str(nb_links))        
        self.global_nb_links += nb_links        


    def display_XMLSpringWebflow_files(self, application, file_full_name):
        
        logging.info('Scanning XML Spring WebFlow files for reference to JSP : ' + str(file_full_name))
        
        tree = ET.parse(file_full_name)
        root = tree.getroot()
           
        print(root.tag)   
        print(root.attrib) # return a dictionary containing the elements 
        
        for flow in root.iter('flow'):
            print(flow.tag)
            print(flow.attrib) # return a dictionary containing the elements 

            for view_state in flow.iter('view-state'):
                print(view_state.tag) # return a dictionary containing the elements 

                print(view_state.attrib) # return a dictionary containing the elements 
                view_state_id = view_state.attrib.get("id")
                logging.info('    view_state_id = '+ view_state_id)
                view_state_view = view_state.attrib.get("view")
                logging.info('    view_state_view = '+ view_state_view)
                view_state_model = view_state.attrib.get("model")
                logging.info('    view_state_model = '+ str(view_state_model)) 


    def file_container(self, myObject):
        object_full_name = myObject.get_fullname()
        logging.info('Object full name = ' + object_full_name) 
        file_path = object_full_name.split(']')[0].replace('[', '')
        logging.info('Object file path = ' + file_path) 
        return file_path
        
    def webapp_container(self, myObject):
        object_full_name = myObject.get_fullname()
        logging.info('Object full name = ' + object_full_name) 
        webapp = object_full_name.split('WEB-INF')[0].replace('[', '')
        logging.info('Object webapp  = ' + webapp) 
        return webapp       

  
    