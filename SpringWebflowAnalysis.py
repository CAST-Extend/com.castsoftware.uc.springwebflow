'''
Created on 2 feb 2017

@author: TGU
'''
import cast.analysers.jee
from cast.analysers import Bookmark
from xml.dom import minidom 
 
class TilesAndSpringWebflowAnalysis(cast.analysers.jee.Extension):
 
    def __init__(self):
        self.NbSpringWebFlowViewStateCreated = 0
        self.NbSpringWebFlowDecisionStateCreated = 0
        self.NbSpringWebFlowActionStateCreated = 0
        self.NbSpringWebFlowOnStartCreated = 0 
        self.NbSpringWebFlowSubFlowStateCreated = 0 
 
    def start_analysis(self,options):
        
        #Save in the _local base the XML files 
        cast.analysers.log.info('Starting Spring WebFlow analysis')
        cast.analysers.log.info('=============== xpath flow ') 
        options.handle_xml_with_xpath('/flow')        # Spring WebFlow definition files
        
        
    def end_analysis(self):
        cast.analysers.log.info('Number of Spring Web Flow view-state objects created : ' + str(self.NbSpringWebFlowViewStateCreated))
        cast.analysers.log.info('Number of Spring Web Flow decision-state objects created : ' + str(self.NbSpringWebFlowDecisionStateCreated))
        cast.analysers.log.info('Number of Spring Web Flow action-state objects created : ' + str(self.NbSpringWebFlowActionStateCreated))
        cast.analysers.log.info('Number of Spring Web Flow on-start objects created : ' + str(self.NbSpringWebFlowOnStartCreated))
        cast.analysers.log.info('Number of Spring Web Flow subflow objects created : ' + str(self.NbSpringWebFlowSubFlowStateCreated))
                
    def start_xml_file(self,file):
        
        xmlfilepath = file.get_path() 
        cast.analysers.log.info('Scanning XML file : ' + xmlfilepath)
        
        if not file.get_path() or len(xmlfilepath.strip()) == 0: 
            return         
               
        if "web.xml" in xmlfilepath or "pom.xml" in xmlfilepath:
            pass    
            
        if '-flux' in xmlfilepath or 'flow' in xmlfilepath: 
            cast.analysers.log.info('Flow a traiter')
            self.analyseXMLSpringWebFlowFile(xmlfilepath, file)
            
    
    def analyseXMLSpringWebFlowFile(self, xmlfilepath, file):        
                 
            cast.analysers.log.info('Scanning XML Spring WebFlow files ... : ' + xmlfilepath)
    
            with minidom.parse(xmlfilepath) as doc: 
                root = doc.documentElement
                
                substitution = {}  
                
                # inherited from generic-flux.xml                 
                substitution['sessionModele'] = 'fr.finances.gouv.cpp.administration.mvc.modele.SessionModele'
                substitution['accueilController'] = 'fr.finances.gouv.cpp.fournisseur.mvc.services.utilisateur.AccueilController'
                substitution['demandePaiementDepot'] = 'fr.finances.gouv.cpp.fournisseur.mvc.modele.facture.SaisieFactureModele' 
                          
                # cxf services 
                # generic way to do it to be implemenented later                 

                substitution['ServiceExposeFacturesRecuesClient'] = 'fr.finances.gouv.cpp.mase.facturerecues.FacturesRecuesSEI'
                substitution['WebParametreApplicatifClient'] = 'fr.finances.gouv.cpp.bat.modele.parametres.ParametreApplicatifSEI'
                substitution['WebServiceAssistanceUtilisateur'] = 'fr.finances.gouv.cpp.assistanceUtilisateur.AssistanceUtilisateurSEI'
                substitution['WebServiceCaptivaClient'] = 'fr.finances.gouv.cpp.facture.service.captiva.createbatch.ICreateBatchService'
                substitution['WebServiceCommunicationClient'] = 'fr.finances.gouv.cpp.bat.modele.parametres.CommunicationSEI'
                substitution['WebServiceDemandePaiementClient'] = 'fr.finances.gouv.cpp.bat.modele.demandedepaiement.FactureSEI'
                substitution['WebServiceFactureAValiderClient'] ='fr.finances.gouv.cpp.bat.modele.demandedepaiement.FactureAValiderSEI'
                substitution['WebServiceFactureRecueClient'] = 'fr.finances.gouv.cpp.bat.modele.demandedepaiement.FactureRecueSEI'
                substitution['WebServiceFactureTravauxClient'] ='fr.finances.gouv.cpp.bat.modele.demandedepaiement.FactureTravauxSEI'
                substitution['WebServiceGestionCompteClient'] = 'fr.finances.gouv.cpp.gestioncompte.gestioncompte.CompteSEI'
                substitution['WebServiceGestionCoordonneesBancairesClient'] = 'fr.finances.gouv.cpp.gestioncompte.gestioncoordonneesbancaires.CoordonneesBancaireSEI'
                substitution['WebServiceGestionEntiteClient'] = 'fr.finances.gouv.cpp.gestioncompte.gestionentite.EntiteSEI'
                substitution['WebServiceGestionEspaceClient'] = 'fr.finances.gouv.cpp.gestioncompte.gestionespace.EspaceSEI'
                substitution['WebServiceGestionMandatClient'] = 'fr.finances.gouv.cpp.gestioncompte.gestionmandat.MandatSEI'
                substitution['WebServiceGestionRattachStructure'] = 'fr.finances.gouv.cpp.administrationGestionnaire.AdministrationSEI'
                substitution['WebServiceGestionServiceClient'] = 'fr.finances.gouv.cpp.gestioncompte.gestionservice.ServiceSEI'
                substitution['WebServiceGestionUtilisateur'] = 'fr.finances.gouv.cpp.administrationGestionnaire.AdministrationSEI'
                substitution['WebServiceInscriptionUtilisateurClient'] = 'fr.finances.gouv.cpp.inscriptionauthentification.UtilisateurSEI'
                substitution['WebServiceParaAppReferentielClient'] = 'fr.finances.gouv.cpp.bat.modele.parametres.ReferentielInterneSEI'
                substitution['WebServiceTexteCommunicationClient'] = 'fr.finances.gouv.cpp.bat.modele.parametres.TexteCommunicationSEI'
                substitution['WebServiceTransverse'] = 'fr.finances.gouv.cpp.transverse.TransverseSEI'
                substitution['creationRemedyService'] = 'fr.finances.gouv.ws.remedy.creation.HPDIncidentInterfaceCreateWSPortTypePortType'
                substitution['depotPortailService'] = 'fr.finances.gouv.ws.archivage.ArchivageCPPPortType'
                substitution['modificationRemedyService']= 'fr.finances.gouv.ws.remedy.modification.HPDIncidentInterfaceWSPortTypePortType'
                substitution['recupService'] = 'fr.finances.gouv.ws.consultation.RecupService'
                substitution['webServiceDemandePaiementClient'] = 'fr.finances.gouv.cpp.bat.modele.demandedepaiement.FactureSEI'
                substitution['webServiceGestionDmdeAccesPortailTiers'] = 'fr.finances.gouv.cpp.gestionaccesportailtiers.DmdeAccesPortailTiersSEI'
                substitution['webServiceGestionDmdeCpteDevSIExterne'] = 'fr.finances.gouv.cpp.gestiondmdecptedev.DmdeCpteDevSIExterneSEI'
                substitution['webServiceGestionFlux'] = 'fr.finances.gouv.cpp.gestionflux.FluxSEI'
                substitution['webServiceGestionFlux'] = 'fr.finances.gouv.cpp.gestionflux.SupervisionSEI'
                substitution['webServiceGestionFluxProd'] = 'fr.finances.gouv.cpp.gestionflux.FluxSEI'
                substitution['webServiceGestionRaccordement'] = 'fr.finances.gouv.cpp.gestionraccordement.RaccordementSEI'
                substitution['webServiceParametresApplicatifClient'] = 'fr.finances.gouv.cpp.bat.modele.parametres.ParametreApplicatifSEI'
                substitution['webServicePieceJointe'] = 'fr.finances.gouv.cpp.bat.modele.piecejointe.PieceJointeSEI'
                substitution['webServiceRechercheHypervision'] = 'fr.finances.gouv.cpp.gestionflux.HypervisionSEI'
                substitution['webServiceReferentielClient'] = 'fr.finances.gouv.cpp.bat.modele.parametres.ReferentielInterneSEI'
                substitution['webServiceSupervision'] = 'fr.finances.gouv.cpp.gestionflux.SupervisionSEI'
                substitution['webserviceAssistanceUtilisateur'] = 'fr.finances.gouv.cpp.assistanceUtilisateur.AssistanceUtilisateurSEI'
                substitution['wsCHO118'] = 'fr.finances.gouv.cpp.metier.ws.cho118.pojo.WsCHO118PortType'
 
 
 
 
 
                for var_substitution in root.getElementsByTagName('var'): 
                    substitution_name = var_substitution.getAttribute('name')
                    cast.analysers.log.info('substitution_name : ' + substitution_name)
                    substitution_class = var_substitution.getAttribute('class')
                    cast.analysers.log.info('substitution_class : ' + substitution_class)
                    substitution[substitution_name] = substitution_class 

                
                for view_state in root.getElementsByTagName('view-state'):
                    view_state_id = view_state.getAttribute('id')
                    cast.analysers.log.info('view-state Id : ' + view_state_id)
                    view_state_view = view_state.getAttribute('view')
                    cast.analysers.log.info('view-state View : ' + view_state_view)
                    view_state_model = view_state.getAttribute('model')
                    cast.analysers.log.info('view-state Model : ' + view_state_model)
                    objectView_State = cast.analysers.CustomObject()
                    objectView_State.set_name(view_state_id)
                    objectView_State.set_type('SpringWebFlowViewState')
                    objectView_State.set_parent(file)
                    objectView_State.save()
                    self.NbSpringWebFlowViewStateCreated += 1                
                    bookmark = Bookmark(file, 1, 1, -1, -1) # TODO : find exact position 
                    objectView_State.save_position(bookmark)
                    objectView_State.save_property('SpringWebFlowViewState.view_state_view', str(view_state_view))
                    objectView_State.save_property('SpringWebFlowViewState.view_state_model', str(view_state_model))
                    
                    for on_entry in view_state.getElementsByTagName('on-entry'):
                        cast.analysers.log.info('==== on entry')

                        list_evaluate_expression = ''
                        
                        for state_evaluate in on_entry.getElementsByTagName('evaluate'):
                            evaluate_expression = state_evaluate.getAttribute('expression')
                            cast.analysers.log.info('======== on-entry evaluate expression avant split : ' + evaluate_expression)
                            if 'T(' in evaluate_expression: 
                                evaluate_expression = evaluate_expression.replace('T(', '')
                                evaluate_expression = evaluate_expression.replace(').', '.')
                            if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                                evaluate_expression = evaluate_expression.split('(')[0] 
                                
                            for var_substitution in substitution:  
                                if evaluate_expression.startswith(var_substitution):
                                    evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    
                                
                            cast.analysers.log.info('======== on-entry evaluate expression : ' + evaluate_expression)
                            #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                            list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
        
                            cast.analysers.log.info('=========== Global on-entry evaluate expression  : ' + list_evaluate_expression)
                        objectView_State.save_property('SpringWebFlowViewState.view_state_on_entry_evaluate', str(list_evaluate_expression))

                    for on_render in view_state.getElementsByTagName('on-render'):
                        cast.analysers.log.info('==== on render')

                        list_evaluate_expression = ''
                        
                        for state_evaluate in on_render.getElementsByTagName('evaluate'):
                            evaluate_expression = state_evaluate.getAttribute('expression')
                            cast.analysers.log.info('======== on-render evaluate expression avant split : ' + evaluate_expression)
                            if 'T(' in evaluate_expression: 
                                evaluate_expression = evaluate_expression.replace('T(', '')
                                evaluate_expression = evaluate_expression.replace(').', '.')
                            if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                                evaluate_expression = evaluate_expression.split('(')[0] 
                                
                            for var_substitution in substitution:  
                                if evaluate_expression.startswith(var_substitution):
                                    evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    
                                
                            cast.analysers.log.info('======== on-render evaluate expression : ' + evaluate_expression)
                            #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                            list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
        
                            cast.analysers.log.info('=========== Global on-render evaluate expression  : ' + list_evaluate_expression)
                        
                        objectView_State.save_property('SpringWebFlowViewState.view_state_on_render_evaluate', str(list_evaluate_expression))
  
  
                    for on_exit in view_state.getElementsByTagName('on-exit'):
                        cast.analysers.log.info('==== on exit')

                        list_evaluate_expression = ''
                        
                        for state_evaluate in on_exit.getElementsByTagName('evaluate'):
                            evaluate_expression = state_evaluate.getAttribute('expression')
                            cast.analysers.log.info('======== on-render evaluate expression avant split : ' + evaluate_expression)
                            if 'T(' in evaluate_expression: 
                                evaluate_expression = evaluate_expression.replace('T(', '')
                                evaluate_expression = evaluate_expression.replace(').', '.')
                            if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                                evaluate_expression = evaluate_expression.split('(')[0] 
                                
                            for var_substitution in substitution:  
                                if evaluate_expression.startswith(var_substitution):
                                    evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    
                                
                            cast.analysers.log.info('======== on-exit evaluate expression : ' + evaluate_expression)
                            #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                            list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
        
                            cast.analysers.log.info('=========== Global on-exit evaluate expression  : ' + list_evaluate_expression)
                        
                        objectView_State.save_property('SpringWebFlowViewState.view_state_on_exit_evaluate', str(list_evaluate_expression))
                                                
                                              
    
                    for transition in view_state.getElementsByTagName('transition'):
                        transition_on = transition.getAttribute('on')
                        cast.analysers.log.info('==== transition on : ' + transition_on)
                        
                        transition_evaluate_expression = ''
                        
                        for evaluate in transition.getElementsByTagName('evaluate'):
                            evaluate_expression = evaluate.getAttribute('expression')
                            cast.analysers.log.info('======== transition evaluate expression avant split : ' + evaluate_expression)
                            if 'T(' in evaluate_expression: 
                                evaluate_expression = evaluate_expression.replace('T(', '')
                                evaluate_expression = evaluate_expression.replace(').', '.')
                            if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                                evaluate_expression = evaluate_expression.split('(')[0] 
                            
                            for var_substitution in substitution:  
                                if evaluate_expression.startswith(var_substitution):
                                    evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    

                            cast.analysers.log.info('======== transition evaluate expression : ' + evaluate_expression)
                            #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                            
                            transition_evaluate_expression = transition_evaluate_expression + evaluate_expression + '#' 
    
                            cast.analysers.log.info('=========== Global transition evaluate expression  : ' + transition_evaluate_expression)
                        objectView_State.save_property('SpringWebFlowViewState.transition_evaluate', str(transition_evaluate_expression))
        
                
                for decision_state in root.getElementsByTagName('decision-state'):
                    decision_state_id = decision_state.getAttribute('id')
                    cast.analysers.log.info('decision_state Id : ' + decision_state_id)
                    objectDecision_State = cast.analysers.CustomObject()
                    objectDecision_State.set_name(decision_state_id)
                    objectDecision_State.set_type('SpringWebFlowDecisionState')
                    objectDecision_State.set_parent(file)
                    objectDecision_State.save()
                    self.NbSpringWebFlowDecisionStateCreated += 1                
                    bookmark = Bookmark(file, 1, 1, -1, -1) # TODO : find exact position 
                    objectDecision_State.save_position(bookmark)
                    for on_entry in decision_state.getElementsByTagName('on-entry'):
                        cast.analysers.log.info('==== on entry')
                        list_evaluate_expression = ''
                        for state_evaluate in on_entry.getElementsByTagName('evaluate'):
                            evaluate_expression = state_evaluate.getAttribute('expression')
                            cast.analysers.log.info('======== evaluate expression avant split : ' + evaluate_expression)
                            if 'T(' in evaluate_expression: 
                                evaluate_expression = evaluate_expression.replace('T(', '')
                                evaluate_expression = evaluate_expression.replace(').', '.')
                            if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                                evaluate_expression = evaluate_expression.split('(')[0] 
                                
                            for var_substitution in substitution:  
                                if evaluate_expression.startswith(var_substitution):
                                    evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    
                                
                            cast.analysers.log.info('======== evaluate expression : ' + evaluate_expression)
                            #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                            list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
        
                            cast.analysers.log.info('=========== Global evaluate expression  : ' + list_evaluate_expression)
                            objectDecision_State.save_property('SpringWebFlowDecisionState.decision_state_evaluate', str(list_evaluate_expression))
                
 
                for action_state in root.getElementsByTagName('action-state'):
                    action_state_id = action_state.getAttribute('id')
                    cast.analysers.log.info('action_state Id : ' + action_state_id)
                    objectAction_State = cast.analysers.CustomObject()
                    objectAction_State.set_name(action_state_id)
                    objectAction_State.set_type('SpringWebFlowActionState')
                    objectAction_State.set_parent(file)
                    objectAction_State.save()
                    self.NbSpringWebFlowActionStateCreated += 1                
                    bookmark = Bookmark(file, 1, 1, -1, -1) # TODO : find exact position 
                    objectAction_State.save_position(bookmark)
                    list_evaluate_expression = ''
                    
                    for on_entry in action_state.getElementsByTagName('transition'):
                        cast.analysers.log.info('==== on entry')
                        for state_evaluate in on_entry.getElementsByTagName('evaluate'):
                            evaluate_expression = state_evaluate.getAttribute('expression')
                            cast.analysers.log.info('======== evaluate expression avant split : ' + evaluate_expression)
                            if 'T(' in evaluate_expression: 
                                evaluate_expression = evaluate_expression.replace('T(', '')
                                evaluate_expression = evaluate_expression.replace(').', '.')
                            if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                                evaluate_expression = evaluate_expression.split('(')[0] 
                            if evaluate_expression == 'java.lang.String': 
                                evaluate_expression = '' 
                                
                            for var_substitution in substitution:  
                                if evaluate_expression.startswith(var_substitution):
                                    evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    
                                
                            cast.analysers.log.info('======== evaluate expression : ' + evaluate_expression)
                            #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                            list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
        
                            cast.analysers.log.info('=========== Global evaluate expression  : ' + list_evaluate_expression)
                            objectAction_State.save_property('SpringWebFlowActionState.transition_evaluate', str(list_evaluate_expression))
                    
                    for state_evaluate in action_state.getElementsByTagName('evaluate'):
                        evaluate_expression = state_evaluate.getAttribute('expression')
                        cast.analysers.log.info('======== evaluate expression avant split : ' + evaluate_expression)
                        if 'T(' in evaluate_expression: 
                            evaluate_expression = evaluate_expression.replace('T(', '')
                            evaluate_expression = evaluate_expression.replace(').', '.')
                        if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                            evaluate_expression = evaluate_expression.split('(')[0] 
                            
                        for var_substitution in substitution:  
                            if evaluate_expression.startswith(var_substitution):
                                evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution], 1)    
                            
                        cast.analysers.log.info('======== evaluate expression : ' + evaluate_expression)
                        #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                        list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
    
                        cast.analysers.log.info('=========== Global evaluate expression  : ' + list_evaluate_expression)
                                    
                    objectAction_State.save_property('SpringWebFlowActionState.action_state_evaluate', str(list_evaluate_expression))
 

                for subflow_state in root.getElementsByTagName('subflow-state'):
                    subflow_state_id = subflow_state.getAttribute('id')
                    cast.analysers.log.info('subflow_state Id : ' + subflow_state_id)
                    objectSubFlow_State = cast.analysers.CustomObject()
                    objectSubFlow_State.set_name(subflow_state_id)
                    objectSubFlow_State.set_type('SpringWebFlowSubFlow')
                    objectSubFlow_State.set_parent(file)
                    objectSubFlow_State.save()
                    self.NbSpringWebFlowSubFlowStateCreated += 1                
                    bookmark = Bookmark(file, 1, 1, -1, -1) # TODO : find exact position 
                    objectSubFlow_State.save_position(bookmark)
                    list_evaluate_expression = ''
                    
                    for on_entry in subflow_state.getElementsByTagName('transition'):
                        cast.analysers.log.info('==== on entry')
                        for state_evaluate in on_entry.getElementsByTagName('evaluate'):
                            evaluate_expression = state_evaluate.getAttribute('expression')
                            cast.analysers.log.info('======== evaluate expression avant split : ' + evaluate_expression)
                            if 'T(' in evaluate_expression: 
                                evaluate_expression = evaluate_expression.replace('T(', '')
                                evaluate_expression = evaluate_expression.replace(').', '.')
                            if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                                evaluate_expression = evaluate_expression.split('(')[0] 
                            if evaluate_expression == 'java.lang.String': 
                                evaluate_expression = '' 
                                
                            for var_substitution in substitution:  
                                if evaluate_expression.startswith(var_substitution):
                                    evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    
                                
                            cast.analysers.log.info('======== evaluate expression : ' + evaluate_expression)
                            #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                            list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
        
                            cast.analysers.log.info('=========== Global evaluate expression  : ' + list_evaluate_expression)
                    
                    objectSubFlow_State.save_property('SpringWebFlowSubFlow.transition_evaluate', str(list_evaluate_expression))
                                    

                for on_start in root.getElementsByTagName('on-start'):
                    objectOnStart = cast.analysers.CustomObject()
                    objectOnStart.set_name("on-start")
                    objectOnStart.set_type('SpringWebFlowOnStart')
                    objectOnStart.set_parent(file)
                    objectOnStart.save()
                    self.NbSpringWebFlowOnStartCreated += 1                
                    bookmark = Bookmark(file, 1, 1, -1, -1) # TODO : find exact position 
                    list_evaluate_expression = ''
                    for state_evaluate in on_start.getElementsByTagName('evaluate'):
                        evaluate_expression = state_evaluate.getAttribute('expression')
                        cast.analysers.log.info('======== evaluate expression avant split : ' + evaluate_expression)
                        if 'T(' in evaluate_expression: 
                            evaluate_expression = evaluate_expression.replace('T(', '')
                            evaluate_expression = evaluate_expression.replace(').', '.')
                        if '(' in evaluate_expression: # only keep classes + method name : no need of the arguments of the method
                            evaluate_expression = evaluate_expression.split('(')[0] 
                            
                        for var_substitution in substitution:  
                            if evaluate_expression.startswith(var_substitution):
                                evaluate_expression = evaluate_expression.replace(var_substitution, substitution[var_substitution])    
                            
                        cast.analysers.log.info('======== evaluate expression : ' + evaluate_expression)
                        #transition_evaluate_expression = transition_evaluate_expression + '#' + evaluate_expression
                        list_evaluate_expression = list_evaluate_expression + evaluate_expression + '#' 
    
                        cast.analysers.log.info('=========== Global evaluate expression  : ' + list_evaluate_expression)
                        objectOnStart.save_property('SpringWebFlowOnStart.on_start_evaluate', str(list_evaluate_expression))
                            
 
                