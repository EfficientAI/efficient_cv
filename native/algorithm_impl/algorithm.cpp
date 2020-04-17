#include <iostream>
#include <vector>
#include <utility>

using namespace std;

vector<float> normalize_data(vector<float> &data){
    vector<float> ret;
    float min_data = data[0], max_data = data[0];
    for(float d : data){
        if(d < min_data){
            min_data = d;
        }
        if(d > max_data){
            max_data = d;
        }
    }
    for(float d : data){
        ret.push_back((d - min_data)/(max_data - min_data));
    }
    return ret;
}

int exit_point_selection(float cpu_load, pair<float, float> &cpu_load_bound,
    vector<pair<int, int> > &runtime_ranges, vector<float> &accuracies, 
    float alpha){
    /*
     * Follows same argument type as that of python definition
    */
    vector<int> predicted_runtimes;
    vector<float> runtime_penalty;
    vector<float> accuracy_penalty;

    int runtime_lower, runtime_upper, increment_scale;
    int predicted_runtime;
    float total_penalty, min_penalty, best_index;
    min_penalty = 1;
    best_index = 0;

    float cpu_load_lower = cpu_load_bound.first;
    float cpu_load_upper = cpu_load_bound.second;
    for(pair<int, int> runtime_bound : runtime_ranges){
        runtime_lower = runtime_bound.first;
        runtime_upper = runtime_bound.second;
        increment_scale = (float)(runtime_upper - runtime_lower);
        increment_scale = increment_scale/(cpu_load_upper - cpu_load_lower);
        increment_scale = (int)(increment_scale*cpu_load);
        predicted_runtime = runtime_lower + increment_scale;
        cout << predicted_runtime << endl;
        predicted_runtimes.push_back(predicted_runtime);
    }
    int ideal_runtime = runtime_ranges[runtime_ranges.size()-1].first;
    float ideal_accuracy = accuracies[accuracies.size()-1];
    for(int index = 0; index<predicted_runtimes.size(); index++){
        int predicted_run = predicted_runtimes[index];
        runtime_penalty.push_back(predicted_run - ideal_runtime);
        accuracy_penalty.push_back(ideal_accuracy - accuracies[index]);
    }
    vector<float> runtime_normalized = normalize_data(runtime_penalty);
    vector<float> accuracy_normalized = normalize_data(accuracy_penalty);
    for(int index=0; index<runtime_normalized.size(); index++){
        total_penalty = alpha*runtime_normalized[index] + 
                            (1.0 - alpha)*accuracy_normalized[index];
        if(total_penalty < min_penalty){
            min_penalty = total_penalty;
            best_index = index;
        }
    }
    return best_index;
}

int main(){
    float cpu_load = 0.9;
    pair<float, float> cpu_load_bound = make_pair(0.2, 0.9);
    vector<pair<int, int> > runtime_ranges = {{20, 40}, {30, 55}, {50, 110},
                                              {70, 140}, {110, 210}, {140, 230}};
    vector<float> accuracies = {60.3, 65.4, 69.8, 71.8, 74.4, 75.0};
    float alpha = 0.40;
    int idx = exit_point_selection(cpu_load, cpu_load_bound, runtime_ranges,
                                   accuracies, alpha);
    cout << idx << endl;
    return 0;
}