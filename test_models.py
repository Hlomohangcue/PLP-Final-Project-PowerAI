"""
Test script to verify pretrained models work correctly with streamlit_app.py
"""
import sys
from pretrained_models import PreTrainedModelLoader

def test_predict_demand():
    """Test the predict_demand method"""
    print("Testing PreTrainedModelLoader.predict_demand()...")
    
    loader = PreTrainedModelLoader()
    
    # Test with different companies
    companies = ['onepower', 'solartech', 'windpower', 'greengrid']
    
    for company in companies:
        print(f"\n{'='*60}")
        print(f"Testing predictions for: {company}")
        print('='*60)
        
        try:
            result = loader.predict_demand(company_id=company, hours_ahead=24)
            
            print(f"✓ Prediction successful!")
            print(f"  - Timestamp: {result['timestamp']}")
            print(f"  - Models used: {', '.join(result['models_used'])}")
            print(f"  - Available predictions: {', '.join(result['predictions'].keys())}")
            
            # Show sample predictions
            for model_name, predictions in result['predictions'].items():
                if predictions:
                    print(f"  - {model_name.upper()}: {len(predictions)} hours predicted")
                    print(f"    First 3 predictions: {predictions[:3]}")
                    
        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    print("PowerAI Model Test Suite")
    print("="*60)
    test_predict_demand()
    print("\n" + "="*60)
    print("Test completed!")
