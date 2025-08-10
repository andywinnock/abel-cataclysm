package com.github.L_Ender.cataclysm.client.model.entity;

import com.github.L_Ender.cataclysm.client.animation.Seedot_Animation;
import com.github.L_Ender.cataclysm.entity.Pet.Seedot_Entity;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.HierarchicalModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;

public class Seedot_Model extends HierarchicalModel<Seedot_Entity> {

    private final ModelPart root;
    private final ModelPart seedot;
    private final ModelPart Head;
    private final ModelPart LeftLeg;
    private final ModelPart RightLeg;

    public Seedot_Model(ModelPart root) {
        this.root = root;
        this.seedot = this.root.getChild("seedot");
        this.Head = this.seedot.getChild("Head");
        this.LeftLeg = this.seedot.getChild("LeftLeg");
        this.RightLeg = this.seedot.getChild("RightLeg");
    }

    public static LayerDefinition createBodyLayer() {
        MeshDefinition meshdefinition = new MeshDefinition();
        PartDefinition partdefinition = meshdefinition.getRoot();

        PartDefinition seedot = partdefinition.addOrReplaceChild("seedot", CubeListBuilder.create(), PartPose.offset(-16.0F, 22.0625F, 0.0F));

        PartDefinition Head = seedot.addOrReplaceChild("Head", CubeListBuilder.create()
                .texOffs(0, 8).addBox(-6.0F, -10.0F, -6.0F, 12.0F, 14.0F, 12.0F, new CubeDeformation(0.0F))
                .texOffs(0, 46).addBox(-1.0F, -13.0F, -1.0F, 2.0F, 3.0F, 2.0F, new CubeDeformation(0.0F))
                .texOffs(29, 32).addBox(-1.0F, 2.0F, -1.0F, 2.0F, 4.0F, 2.0F, new CubeDeformation(0.0F))
                .texOffs(0, -10).addBox(-7.0F, -7.0F, -7.25F, 14.0F, 3.0F, 14.0F, new CubeDeformation(0.0F)),
                PartPose.offset(10.0F, -5.0625F, 6.0F));

        PartDefinition LeftLeg = seedot.addOrReplaceChild("LeftLeg", CubeListBuilder.create(), PartPose.offsetAndRotation(16.0F, 1.9375F, 0.0F, 0.0F, -0.1745F, 0.0F));

        PartDefinition left_leg_r1 = LeftLeg.addOrReplaceChild("left_leg_r1", CubeListBuilder.create()
                .texOffs(21, 55).addBox(-4.0F, -3.0F, 0.0F, 4.0F, 3.0F, 6.0F, new CubeDeformation(0.0F)),
                PartPose.offsetAndRotation(2.0F, 0.0F, 4.0F, 0.0F, -0.2182F, 0.0F));

        PartDefinition RightLeg = seedot.addOrReplaceChild("RightLeg", CubeListBuilder.create(), PartPose.offsetAndRotation(16.0F, 1.9375F, 0.0F, 0.0F, 0.1745F, 0.0F));

        PartDefinition right_leg_r1 = RightLeg.addOrReplaceChild("right_leg_r1", CubeListBuilder.create()
                .texOffs(0, 55).addBox(-4.0F, -3.0F, 0.0F, 4.0F, 3.0F, 6.0F, new CubeDeformation(0.0F)),
                PartPose.offsetAndRotation(-10.0F, 0.0F, 1.0F, 0.0F, 0.2182F, 0.0F));

        return LayerDefinition.create(meshdefinition, 64, 64);
    }

    @Override
    public void setupAnim(Seedot_Entity entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch) {
        this.root().getAllParts().forEach(ModelPart::resetPose);
        this.animateHeadLookTarget(netHeadYaw, headPitch);
        this.animate(entity.getAnimationState("idle"), Seedot_Animation.IDLE, ageInTicks, 1.0F);
        this.animate(entity.getAnimationState("walk"), Seedot_Animation.WALK, ageInTicks, 1.0F);
        this.animate(entity.getAnimationState("sit"), Seedot_Animation.SIT, ageInTicks, 1.0F);
        this.animateWalk(Seedot_Animation.WALK, limbSwing, limbSwingAmount, 2.0F, 2.5F);
    }

    private void animateHeadLookTarget(float yRot, float xRot) {
        this.Head.xRot = xRot * ((float) Math.PI / 180F);
        this.Head.yRot = yRot * ((float) Math.PI / 180F);
    }

    public ModelPart root() {
        return this.root;
    }

    @Override
    public void renderToBuffer(PoseStack poseStack, VertexConsumer vertexConsumer, int packedLight, int packedOverlay, float red, float green, float blue, float alpha) {
        root.render(poseStack, vertexConsumer, packedLight, packedOverlay, red, green, blue, alpha);
    }
}