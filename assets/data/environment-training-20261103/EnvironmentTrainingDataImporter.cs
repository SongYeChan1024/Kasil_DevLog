#if UNITY_EDITOR
using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine.SceneManagement;
using Newtonsoft.Json;

// Created for the 2026-11-03 environment data archive. Uses no sample-project source code.
// Place this file in Assets/Editor in a URP project, then choose Tools/Environment Training Data/Import Presets.
public static class EnvironmentTrainingDataImporter
{
    [Serializable] public class Data { public int formatVersion; public string unityVersion, urpVersion; public LightData[] lights; public ProfileData[] profiles; }
    [Serializable] public class LightData
    {
        public string name, sourceHierarchy, type, bakeMode, shadows;
        public float intensity, range, spotAngle, innerSpotAngle, shadowStrength, shadowBias, shadowNormalBias, shadowNearPlane, bounceIntensity, colorTemperature;
        public int lightUnit;
        public bool useColorTemperature; public float[] color, rotation, areaSize;
    }
    [Serializable] public class ProfileData { public string name, sourcePath; public ComponentData[] components; }
    [Serializable] public class ComponentData { public string type; public bool active; public PropertyData[] properties; }
    [Serializable] public class PropertyData { public string path, kind, text, guid; public double number; public bool boolean; public float[] numbers; }

    [MenuItem("Tools/Environment Training Data/Import Presets")]
    static void ImportMenu()
    {
        var path=EditorUtility.OpenFilePanel("Select portable-presets.json",Application.dataPath,"json");
        if(string.IsNullOrEmpty(path))return;
        var folder="Assets/EnvironmentTrainingData_"+DateTime.UtcNow.ToString("yyyyMMdd_HHmmss");
        Debug.Log(ImportData(path,folder));
        EditorUtility.DisplayDialog("Environment Training Data","New presets created in "+folder+". Read ImportReport.txt for skipped references. Existing scenes and pipeline settings were not changed.","OK");
    }

    public static string ImportData(string jsonPath,string outputFolder)
    {
        var data=JsonConvert.DeserializeObject<Data>(File.ReadAllText(jsonPath));
        if(data==null||data.formatVersion!=1||data.lights==null||data.profiles==null)throw new InvalidOperationException("Unsupported preset JSON: version="+(data==null?-1:data.formatVersion)+", lights="+(data?.lights?.Length??-1)+", profiles="+(data?.profiles?.Length??-1));
        if(!outputFolder.StartsWith("Assets/",StringComparison.Ordinal)||outputFolder.Contains("..")||AssetDatabase.IsValidFolder(outputFolder))throw new InvalidOperationException("Choose a new folder under Assets; existing assets are never overwritten");
        EnsureFolder(outputFolder);EnsureFolder(outputFolder+"/Lights");EnsureFolder(outputFolder+"/Volumes");
        var report=new List<string>{"Source Unity "+data.unityVersion+", URP "+data.urpVersion,"Only new assets created. No pipeline assignment, scene connection, bake, scripts or shader installation.","Light prefabs preserve base Light settings, not cookies, URP extensions, source positions, or runtime controllers."};
        var scene=EditorSceneManager.NewPreviewScene();int lights=0,profiles=0,skipped=0;
        try
        {
            foreach(var item in data.lights)
            {
                var go=new GameObject(SafeName(item.name));SceneManager.MoveGameObjectToScene(go,scene);
                try
                {
                    var light=go.AddComponent<Light>();light.type=(LightType)Enum.Parse(typeof(LightType),item.type);
                    light.lightmapBakeType=(LightmapBakeType)Enum.Parse(typeof(LightmapBakeType),item.bakeMode);
                    var lightProperties=new SerializedObject(light);var unit=lightProperties.FindProperty("m_LightUnit");if(unit!=null){unit.intValue=item.lightUnit;lightProperties.ApplyModifiedPropertiesWithoutUndo();}
                    light.color=new Color(item.color[0],item.color[1],item.color[2],item.color[3]);light.intensity=item.intensity;light.range=item.range;
                    if(item.areaSize!=null&&item.areaSize.Length==2)light.areaSize=new Vector2(item.areaSize[0],item.areaSize[1]);
                    light.spotAngle=item.spotAngle;light.innerSpotAngle=item.innerSpotAngle;light.shadows=(LightShadows)Enum.Parse(typeof(LightShadows),item.shadows);
                    light.shadowStrength=item.shadowStrength;light.shadowBias=item.shadowBias;light.shadowNormalBias=item.shadowNormalBias;light.shadowNearPlane=item.shadowNearPlane;light.bounceIntensity=item.bounceIntensity;
                    light.useColorTemperature=item.useColorTemperature;light.colorTemperature=item.colorTemperature;
                    go.transform.position=new Vector3(0,2,0);go.transform.rotation=Quaternion.Euler(item.rotation[0],item.rotation[1],item.rotation[2]);
                    PrefabUtility.SaveAsPrefabAsset(go,outputFolder+"/Lights/"+go.name+".prefab");lights++;
                }
                finally{UnityEngine.Object.DestroyImmediate(go);}
            }
        }
        finally{EditorSceneManager.ClosePreviewScene(scene);}
        foreach(var item in data.profiles)
        {
            var profile=ScriptableObject.CreateInstance<VolumeProfile>();profile.name=SafeName(item.name);
            AssetDatabase.CreateAsset(profile,outputFolder+"/Volumes/"+profile.name+".asset");
            foreach(var componentData in item.components)
            {
                var type=AppDomain.CurrentDomain.GetAssemblies().Select(a=>a.GetType(componentData.type,false)).FirstOrDefault(t=>t!=null);
                if(type==null||!typeof(VolumeComponent).IsAssignableFrom(type)){report.Add("Missing Volume type: "+componentData.type+" in "+item.name);skipped++;continue;}
                var component=(VolumeComponent)ScriptableObject.CreateInstance(type);component.name=type.Name;component.active=componentData.active;
                AssetDatabase.AddObjectToAsset(component,profile);profile.components.Add(component);
                var serialized=new SerializedObject(component);
                foreach(var value in componentData.properties)
                {
                    var property=serialized.FindProperty(value.path);
                    if(property==null||!Apply(property,value)){report.Add("Skipped "+item.name+"/"+type.Name+"/"+value.path+" ("+value.kind+")");skipped++;}
                }
                serialized.ApplyModifiedPropertiesWithoutUndo();EditorUtility.SetDirty(component);AssetDatabase.SaveAssetIfDirty(component);
            }
            EditorUtility.SetDirty(profile);AssetDatabase.SaveAssetIfDirty(profile);profiles++;
        }
        report.Add("Created light prefabs: "+lights+"; Volume profiles: "+profiles+"; skipped properties/types: "+skipped);
        File.WriteAllLines(outputFolder+"/ImportReport.txt",report);AssetDatabase.ImportAsset(outputFolder+"/ImportReport.txt");
        return report[report.Count-1];
    }
    static bool Apply(SerializedProperty p,PropertyData value)
    {
        if(value.kind=="Boolean"&&p.propertyType==SerializedPropertyType.Boolean){p.boolValue=value.boolean;return true;}
        if(value.kind=="String"&&p.propertyType==SerializedPropertyType.String){p.stringValue=value.text;return true;}
        if(value.kind=="Number"||value.kind=="Enum")
        {
            if(p.propertyType==SerializedPropertyType.Float){p.doubleValue=value.number;return true;}
            if(p.propertyType==SerializedPropertyType.Integer||p.propertyType==SerializedPropertyType.Enum){p.intValue=(int)value.number;return true;}
        }
        if(value.kind=="Null"&&p.propertyType==SerializedPropertyType.ObjectReference){p.objectReferenceValue=null;return true;}
        if(value.kind=="Reference"&&p.propertyType==SerializedPropertyType.ObjectReference)
        {
            var path=AssetDatabase.GUIDToAssetPath(value.guid);if(string.IsNullOrEmpty(path))return false;
            var asset=AssetDatabase.LoadMainAssetAtPath(path);if(!asset)return false;p.objectReferenceValue=asset;return true;
        }
        if(value.kind=="Vector"&&value.numbers!=null)
        {
            var v=value.numbers;
            if(p.propertyType==SerializedPropertyType.Color&&v.Length==4){p.colorValue=new Color(v[0],v[1],v[2],v[3]);return true;}
            if(p.propertyType==SerializedPropertyType.Vector4&&v.Length==4){p.vector4Value=new Vector4(v[0],v[1],v[2],v[3]);return true;}
            if(p.propertyType==SerializedPropertyType.Vector3&&v.Length==3){p.vector3Value=new Vector3(v[0],v[1],v[2]);return true;}
            if(p.propertyType==SerializedPropertyType.Vector2&&v.Length==2){p.vector2Value=new Vector2(v[0],v[1]);return true;}
        }
        return false;
    }
    static void EnsureFolder(string path){if(AssetDatabase.IsValidFolder(path))return;var parent=path.Substring(0,path.LastIndexOf('/'));EnsureFolder(parent);AssetDatabase.CreateFolder(parent,path.Substring(path.LastIndexOf('/')+1));}
    static string SafeName(string name){foreach(var c in Path.GetInvalidFileNameChars())name=name.Replace(c,'_');return name;}
}
#endif
