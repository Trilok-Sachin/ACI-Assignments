% Decision tree rules
predict_location(LakeDistance, RiverDistance, RainfallIntensity, SandyAquifer, BeachDistance, Location) :-
    (   LakeDistance < 10 ->
        Location = lake
    ;   (   RiverDistance < 8 ->
            (   RainfallIntensity < 200 ->
                Location = river
            ;   Location = rain
            )
        ;   (   RainfallIntensity >= 150 ->
                Location = rain
            ;   (   SandyAquifer == true ->
                    (   BeachDistance < 5 ->
                        (   RiverDistance < 20 ->
                            Location = river
                        ;   Location = rain
                        )
                    ;   Location = groundwater
                    )
                ;   (   LakeDistance >= 14 ->
                        Location = rain
                    ;   Location = lake
                    )
                )
            )
        )
    ).